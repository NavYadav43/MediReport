# reports/gemini_service.py
# ML-powered medical report analyzer — no API, no internet required

import re
import json
import os
import numpy as np
from .medical_knowledge import PARAMETERS, REPORT_CATEGORY_MAP
from .ml_trainer import train_models, load_models, models_exist

RISK_LABELS = {0: "low", 1: "medium", 2: "high", 3: "critical"}


def extract_text_from_pdf(file_path):
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
    except Exception:
        text = ""
    return text


def extract_text_from_image(file_path):
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception:
        return ""


def extract_values_from_text(text):
    extracted = {}
    text_lower = text.lower()
    for param, info in PARAMETERS.items():
        aliases = info.get("aliases", [param])
        for alias in aliases:
            pattern = re.compile(
                r'(?i)' + re.escape(alias) + r'[\s:=\-]*(\d+\.?\d*)',
                re.IGNORECASE
            )
            match = pattern.search(text_lower)
            if match:
                try:
                    value = float(match.group(1))
                    extracted[param] = value
                    break
                except ValueError:
                    continue
    return extracted


def predict_risk(extracted_values):
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
            positive_notes.append(f"{param.replace('_', ' ').title()}: {value} {unit} — within normal range ✅")
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


def analyze_medical_report(file_path: str, file_type: str, report_type: str = 'other') -> dict:
    if file_type == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type in ['jpg', 'jpeg', 'png', 'webp']:
        text = extract_text_from_image(file_path)
        if not text:
            return {
                "summary": "Image report uploaded. For best results, please use the 'Analyze Manually' button to enter your values directly. Our ML engine will analyze them instantly.",
                "report_detected_type": report_type.replace("_", " ").title(),
                "risk_level": "low",
                "key_findings": [],
                "medications": [],
                "precautions": [{"title": "Use Manual Entry", "description": "Click 'Analyze Manually' on this page to enter report values for ML analysis."}],
                "prevention": [],
                "lifestyle_advice": [],
                "when_to_see_doctor": [],
                "dietary_restrictions": [],
                "positive_notes": [],
                "disclaimer": "This ML analysis is for informational purposes only. Always consult a qualified doctor.",
                "extracted_values": {}
            }
    else:
        text = ""

    extracted_values = extract_values_from_text(text)

    if not extracted_values:
        return {
            "summary": "Could not automatically extract values from this report. Please use 'Analyze Manually' to enter your values for instant ML analysis.",
            "report_detected_type": report_type.replace("_", " ").title(),
            "risk_level": "low",
            "key_findings": [],
            "medications": [],
            "precautions": [{"title": "Manual Entry Required", "description": "Use the manual entry form to type your report values. Works for all report types."}],
            "prevention": [{"title": "Use Text-Based PDFs", "description": "Text-based PDFs work best for automatic extraction. Scanned reports need manual entry."}],
            "lifestyle_advice": [],
            "when_to_see_doctor": [],
            "dietary_restrictions": [],
            "positive_notes": [],
            "disclaimer": "This ML analysis is for informational purposes only. Always consult a qualified doctor.",
            "extracted_values": {}
        }

    try:
        risk_level, _ = predict_risk(extracted_values)
    except Exception:
        risk_level = "medium"

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
        "disclaimer": "This analysis is generated by a locally trained ML model using WHO/NIH medical standards. It is for informational purposes only and does not replace professional medical advice. Always consult a qualified healthcare provider.",
        "extracted_values": extracted_values,
    }


# ─── MEDIBOT CHAT ─────────────────────────────────────────────────────────────

MEDICAL_QA = {
    "blood pressure": "Normal blood pressure is below 120/80 mmHg. 130/80 or higher is hypertension. Manage with low-salt diet, exercise, and doctor guidance.",
    "diabetes": "Fasting blood sugar above 126 mg/dL indicates diabetes. Between 100-125 is prediabetes. Manage with diet, exercise, and medication if prescribed.",
    "cholesterol": "Total cholesterol should be under 200 mg/dL. LDL (bad) below 100. HDL (good) above 40. Manage with diet, exercise, and statins if prescribed.",
    "thyroid": "TSH between 0.4-4.0 is normal. High TSH = hypothyroidism. Low TSH = hyperthyroidism. Both are treatable with medication.",
    "hemoglobin": "Normal hemoglobin is 12-17.5 g/dL. Low = anemia. Eat iron-rich foods like spinach, lentils, and consult your doctor.",
    "kidney": "Creatinine above 1.2 mg/dL may indicate kidney stress. Stay hydrated, limit salt/protein, avoid NSAIDs.",
    "triglycerides": "Triglycerides under 150 mg/dL is normal. High levels caused by sugar and alcohol. Reduce both and exercise regularly.",
    "anemia": "Anemia means low hemoglobin or RBC. Common causes: iron deficiency, B12 deficiency, blood loss. Eat iron-rich foods and see your doctor.",
    "wbc": "Normal WBC is 4000-11000 cells/µL. High WBC suggests infection. Low WBC weakens immunity. See a doctor for either extreme.",
    "platelet": "Normal platelets: 150,000-400,000. Low = risk of bleeding. High = risk of clotting. Both need medical evaluation.",
    "urine": "Normal urine should have no glucose, protein, or bacteria. Presence of these indicates kidney, bladder, or metabolic issues.",
    "normal": "Normal ranges vary by age, gender, and lab. Always compare your results with the reference range on your report and consult your doctor.",
}


def chat_with_ai(message: str, context: str = "", report_context: dict = None) -> str:
    message_lower = message.lower()

    if report_context and report_context.get("key_findings"):
        risk = report_context.get("risk_level", "unknown")
        abnormal = [f for f in report_context.get("key_findings", []) if f.get("status") != "normal"]
        if any(word in message_lower for word in ["my report", "my result", "what does", "explain", "this report", "my test", "analyze"]):
            if abnormal:
                params = ", ".join([f["parameter"] for f in abnormal[:3]])
                return (f"Based on your uploaded report, I found **{len(abnormal)} abnormal parameter(s)**: {params}.\n\n"
                        f"Your overall risk level is **{risk.upper()}**.\n\n"
                        f"Please scroll up to see the detailed analysis with medications, precautions, and lifestyle advice. "
                        f"Remember to consult your doctor for proper diagnosis and treatment.")
            else:
                return ("Great news! Your report shows all parameters within normal range. "
                        f"Your risk level is **LOW**. Keep up your healthy lifestyle! Regular checkups are still recommended.")

    for keyword, answer in MEDICAL_QA.items():
        if keyword in message_lower:
            return f"**{keyword.title()}:**\n\n{answer}\n\n⚕️ *Always consult a qualified doctor for personalized medical advice.*"

    if any(word in message_lower for word in ["hi", "hello", "hey", "namaste"]):
        return ("👋 Hello! I'm **MediBot**, your AI health assistant.\n\n"
                "I can help you:\n• Understand your medical report results\n"
                "• Explain medical terms in simple language\n"
                "• Answer general health questions\n\nUpload a report or type your question!")

    if any(word in message_lower for word in ["thank", "thanks", "helpful"]):
        return "You're welcome! 😊 Always consult a qualified doctor for personalized advice. Stay healthy!"

    return (f"I can help with questions about:\n"
            "• Blood test values (hemoglobin, WBC, glucose, platelets)\n"
            "• Lipid profile (cholesterol, triglycerides, HDL, LDL)\n"
            "• Thyroid function (TSH, T3, T4)\n"
            "• Urine test & kidney function\n"
            "• General health and lifestyle\n\n"
            "Try: *'What does high cholesterol mean?'* or *'Explain my report'*\n\n"
            "⚕️ *For specific medical advice, always consult your doctor.*")
