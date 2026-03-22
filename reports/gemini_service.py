# reports/gemini_service.py
# ML-powered medical report analyzer — no API, no internet required

import re
import json
import os
import numpy as np
from .medical_knowledge import PARAMETERS, REPORT_CATEGORY_MAP
from .ml_trainer import train_models, load_models, models_exist

RISK_LABELS = {0: "low", 1: "medium", 2: "high", 3: "critical"}


# ─── PDF TEXT EXTRACTION ─────────────────────────────────────────────────────

def extract_text_from_pdf(file_path):
    """Extract text from PDF using pdfplumber."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except ImportError:
        try:
            with open(file_path, 'rb') as f:
                raw = f.read().decode('latin-1', errors='ignore')
            parts = re.findall(r'\(([^)]{2,50})\)', raw)
            text = ' '.join(parts)
        except Exception:
            text = ""
    except Exception as e:
        text = ""
    return text


def extract_text_from_image(file_path):
    """Try OCR on image files using pytesseract."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception:
        return ""


# ─── IMPROVED VALUE EXTRACTION ───────────────────────────────────────────────

# Smarter patterns per parameter — allows brackets, spaces, units between name and value
EXTRACTION_PATTERNS = {
    "hemoglobin":       [r'h(?:a?emoglobin|gb?)\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "wbc":              [r'w\.?b\.?c\.?(?:\s*count)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'(?:white\s*blood\s*(?:cell|count)|leukocyte|tlc)\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "platelets":        [r'platelet(?:\s*count)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'plt\b[^\d\n]{0,20}(\d+\.?\d*)'],
    "rbc":              [r'r\.?b\.?c\.?(?:\s*count)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'(?:red\s*blood\s*(?:cell|count)|erythrocyte)\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "fasting_glucose":  [r'(?:fasting\s*(?:blood\s*)?(?:sugar|glucose)|f\.?b\.?s\.?|blood\s*glucose\s*fasting)\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "total_cholesterol":[r'total\s*cholesterol\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'(?<!hdl\s)(?<!ldl\s)cholesterol\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "hdl":              [r'h\.?d\.?l\.?(?:[\s\-]*c(?:holesterol)?)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'good\s*cholesterol\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "ldl":              [r'l\.?d\.?l\.?(?:[\s\-]*c(?:holesterol)?)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'bad\s*cholesterol\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "triglycerides":    [r'triglyceride[s]?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'\btr?g\b[^\d\n]{0,20}(\d+\.?\d*)'],
    "tsh":              [r't\.?s\.?h\.?(?:\s*level)?\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'thyroid\s*stimulating\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "t3":               [r'\bt\.?3\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'triiodothyronine\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "t4":               [r'\bt\.?4\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'thyroxine\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "urine_glucose":    [r'(?:urine|urinary)\s*(?:glucose|sugar)\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "urine_protein":    [r'(?:urine|urinary)\s*protein\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r'proteinuria\b[^\d\n]{0,40}(\d+\.?\d*)'],
    "urine_ph":         [r'(?:urine\s*)?p\.?h\.?\b[^\d\n]{0,20}(\d+\.?\d*)'],
    "creatinine":       [r'(?:serum\s*)?creatinine\b[^\d\n]{0,40}(\d+\.?\d*)',
                         r's\.?\s*creatinine\b[^\d\n]{0,40}(\d+\.?\d*)'],
}


def extract_values_from_text(text):
    """
    Extract numeric parameter values from report text.
    Uses smarter regex that handles brackets, units, and varied spacing.
    """
    extracted = {}
    text_lower = text.lower()

    for param, patterns in EXTRACTION_PATTERNS.items():
        for pattern in patterns:
            try:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    # Sanity check: reject obviously wrong values
                    low, high = PARAMETERS[param]["normal"]
                    max_allowed = high * 20 if high > 0 else 1000
                    if 0 <= value <= max_allowed:
                        extracted[param] = value
                        break
            except (ValueError, AttributeError):
                continue

    return extracted


# ─── ML PREDICTION ───────────────────────────────────────────────────────────

def predict_risk(extracted_values):
    """Use trained Random Forest to predict overall risk level."""
    if not models_exist():
        print("Training ML models for the first time...")
        train_models()

    rf_model, scaler, param_list = load_models()

    feature_vector = []
    for param in param_list:
        if param in extracted_values:
            feature_vector.append(extracted_values[param])
        else:
            low, high = PARAMETERS[param]["normal"]
            midpoint = (low + high) / 2 if high > 0 else 0
            feature_vector.append(midpoint)

    X = np.array([feature_vector])
    X_scaled = scaler.transform(X)
    risk_num = rf_model.predict(X_scaled)[0]
    probabilities = rf_model.predict_proba(X_scaled)[0]
    return RISK_LABELS[int(risk_num)], probabilities


# ─── FINDINGS GENERATOR ──────────────────────────────────────────────────────

def generate_findings(extracted_values):
    key_findings = []
    medications = []
    precautions = []
    prevention = []
    lifestyle_advice = []
    when_to_see_doctor = []
    dietary_restrictions = []
    positive_notes = []
    seen_meds = set()
    seen_precautions = set()
    seen_prevention = set()

    for param, value in extracted_values.items():
        if param not in PARAMETERS:
            continue
        info = PARAMETERS[param]
        low, high = info["normal"]
        unit = info["unit"]

        if high == 0:
            status = "high" if value > 0 else "normal"
        elif value < low:
            status = "low"
        elif value > high:
            status = "high"
        else:
            status = "normal"

        normal_range = f"{low}–{high} {unit}" if high > 0 else f"0 {unit} (absent)"

        if status == "normal":
            positive_notes.append(
                f"{param.replace('_', ' ').title()}: {value} {unit} — within normal range ✅"
            )
            key_findings.append({
                "parameter": param.replace("_", " ").title(),
                "value": f"{value} {unit}",
                "normal_range": normal_range,
                "status": "normal",
                "interpretation": "Value is within the healthy normal range."
            })
            continue

        advice_key = f"{status}_advice"
        advice = info.get(advice_key, {})
        condition_name = advice.get("name", f"Abnormal {param.replace('_', ' ').title()}")

        key_findings.append({
            "parameter": param.replace("_", " ").title(),
            "value": f"{value} {unit}",
            "normal_range": normal_range,
            "status": status,
            "interpretation": f"{condition_name} detected. Please review with your doctor."
        })

        for med in advice.get("medications", []):
            if med["name"] not in seen_meds:
                medications.append(med)
                seen_meds.add(med["name"])

        for prec in advice.get("precautions", []):
            if prec["title"] not in seen_precautions:
                precautions.append(prec)
                seen_precautions.add(prec["title"])

        for prev in advice.get("prevention", []):
            if prev["title"] not in seen_prevention:
                prevention.append(prev)
                seen_prevention.add(prev["title"])

        lifestyle_advice.extend(advice.get("lifestyle", []))
        when_to_see_doctor.extend(advice.get("doctor_signs", []))

    # Dietary restrictions
    for param, value in extracted_values.items():
        if param not in PARAMETERS:
            continue
        low, high = PARAMETERS[param]["normal"]
        if high > 0 and value > high:
            if param in ["total_cholesterol", "ldl", "triglycerides"]:
                dietary_restrictions.append("Avoid fried foods, butter, and full-fat dairy")
                dietary_restrictions.append("Limit red meat and processed meats")
            if param == "fasting_glucose":
                dietary_restrictions.append("Avoid sugar, sweets, soft drinks, and refined carbohydrates")
                dietary_restrictions.append("Limit white rice, white bread, and maida products")
            if param in ["urine_protein", "creatinine"]:
                dietary_restrictions.append("Reduce salt (sodium) intake strictly")
                dietary_restrictions.append("Limit protein supplements and excessive red meat")
            if param == "triglycerides":
                dietary_restrictions.append("Eliminate alcohol completely")

    return {
        "key_findings": key_findings,
        "medications": medications,
        "precautions": precautions,
        "prevention": prevention,
        "lifestyle_advice": lifestyle_advice[:8],
        "when_to_see_doctor": list(set(when_to_see_doctor))[:8],
        "dietary_restrictions": list(set(dietary_restrictions)),
        "positive_notes": positive_notes,
    }


def generate_summary(extracted_values, risk_level, report_type):
    total = len(extracted_values)
    abnormal = sum(
        1 for param, value in extracted_values.items()
        if param in PARAMETERS and (
            (value < PARAMETERS[param]["normal"][0] and PARAMETERS[param]["normal"][0] > 0) or
            (PARAMETERS[param]["normal"][1] > 0 and value > PARAMETERS[param]["normal"][1]) or
            (PARAMETERS[param]["normal"][1] == 0 and value > 0)
        )
    )
    type_label = report_type.replace("_", " ").title()
    if risk_level == "low":
        return (f"Your {type_label} report shows {total} parameters analyzed, all within normal healthy ranges. "
                f"Your results look great! Continue maintaining your current healthy lifestyle.")
    elif risk_level == "medium":
        return (f"Your {type_label} report shows {total} parameters analyzed. "
                f"{abnormal} parameter(s) are slightly outside the normal range. "
                f"These findings need attention but are manageable with lifestyle changes and medical guidance.")
    elif risk_level == "high":
        return (f"Your {type_label} report shows {abnormal} out of {total} parameters with significant abnormalities. "
                f"Please consult your doctor soon for proper evaluation and treatment planning.")
    else:
        return (f"Your {type_label} report shows {abnormal} critical abnormalities requiring immediate medical attention. "
                f"Please visit a doctor or hospital as soon as possible.")


# ─── MAIN ANALYSIS FUNCTION ──────────────────────────────────────────────────

def analyze_medical_report(file_path: str, file_type: str, report_type: str = 'other') -> dict:
    """Extract values from report file, run ML, return full analysis."""

    # Step 1: Extract text
    if file_type == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type in ['jpg', 'jpeg', 'png', 'webp']:
        text = extract_text_from_image(file_path)
    else:
        text = ""

    # Step 2: Extract values
    extracted_values = extract_values_from_text(text) if text.strip() else {}

    # Step 3: If nothing extracted, return helpful guidance
    if not extracted_values:
        tip = ("The PDF appears to be a scanned image. For accurate ML analysis, "
               "please use 'Enter Values Manually' and type the values from your report.")
        if file_type in ['jpg', 'jpeg', 'png', 'webp']:
            tip = "Image files need manual value entry. Please click 'Enter Values Manually' and type your values."

        return {
            "summary": f"Could not auto-extract values. {tip}",
            "report_detected_type": report_type.replace("_", " ").title(),
            "risk_level": "low",
            "key_findings": [],
            "medications": [],
            "precautions": [{"title": "Use Manual Entry for Best Results",
                             "description": tip}],
            "prevention": [{"title": "Text-Based PDFs Work Best",
                            "description": "If your PDF was generated digitally (not scanned), values can be auto-extracted."}],
            "lifestyle_advice": [],
            "when_to_see_doctor": [],
            "dietary_restrictions": [],
            "positive_notes": [],
            "disclaimer": "This ML analysis is for informational purposes only. Always consult a qualified doctor.",
            "extracted_values": {}
        }

    # Step 4: ML risk prediction
    try:
        risk_level, _ = predict_risk(extracted_values)
    except Exception:
        risk_level = "medium"

    # Step 5: Generate findings and summary
    findings = generate_findings(extracted_values)
    summary = generate_summary(extracted_values, risk_level, report_type)

    return {
        "summary": summary,
        "report_detected_type": report_type.replace("_", " ").title(),
        "risk_level": risk_level,
        "key_findings": findings["key_findings"],
        "medications": findings["medications"],
        "precautions": findings["precautions"],
        "prevention": findings["prevention"],
        "lifestyle_advice": findings["lifestyle_advice"],
        "when_to_see_doctor": findings["when_to_see_doctor"],
        "dietary_restrictions": findings["dietary_restrictions"],
        "positive_notes": findings["positive_notes"],
        "disclaimer": ("This analysis is generated by a locally trained ML model using WHO/NIH medical standards. "
                       "It is for informational purposes only and does not replace professional medical advice. "
                       "Always consult a qualified healthcare provider."),
        "extracted_values": extracted_values,
    }


# ─── MEDIBOT CHAT — HYBRID (Gemini first, ML fallback) ───────────────────────

def chat_with_ai(message: str, context: str = "", report_context: dict = None) -> str:
    """
    Hybrid chatbot:
    1. Try Gemini API first (best quality answers)
    2. If Gemini fails (rate limit, no API key, network error) → fall back to ML TF-IDF
    3. User never sees an error
    """
    from django.conf import settings
    from .ml_chatbot import ml_chat_response

    api_key = getattr(settings, 'GEMINI_API_KEY', '')

    # Try Gemini first if API key is configured
    if api_key:
        try:
            response = _gemini_chat(message, context, report_context, api_key)
            if response:
                return response
        except Exception:
            pass  # Silently fall back to ML

    # ML fallback — always works offline
    return ml_chat_response(message, report_context=report_context)


def _gemini_chat(message: str, context: str, report_context: dict, api_key: str) -> str:
    """Call Gemini API for chat. Returns None on any failure."""
    import urllib.request
    import urllib.error

    system_context = """You are MediBot, a friendly medical AI assistant for MediReport.
Help users understand medical reports and answer health questions.
- Be warm, empathetic, reassuring
- Use simple language everyone can understand
- Always recommend consulting a real doctor
- Never diagnose or prescribe
- Keep responses concise (2-4 paragraphs)
- Use bullet points for lists"""

    if report_context:
        system_context += f"\n\nUser report analysis:\n{json.dumps(report_context, indent=2)[:800]}"
    if context:
        system_context += f"\n\nRecent conversation:\n{context}"

    full_message = f"{system_context}\n\nUser: {message}\n\nMediBot:"

    payload = json.dumps({
        "contents": [{"parts": [{"text": full_message}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512}
    }).encode('utf-8')

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return None  # Rate limit — trigger ML fallback
        return None
    except Exception:
        return None
