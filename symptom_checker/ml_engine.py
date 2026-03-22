# symptom_checker/ml_engine.py
# TF-IDF + scoring ML engine for symptom-condition matching

import os
import pickle
import numpy as np
from .symptom_data import CONDITIONS, SYMPTOMS, RED_FLAG_COMBOS

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'symptom_model.pkl')


def train_symptom_model():
    """Train a symptom-condition matching model."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Build symptom vectors for each condition
    condition_symptom_texts = {}
    for cond_id, cond in CONDITIONS.items():
        # Weight key symptoms higher by repeating them
        symptoms_text = ' '.join(cond['key_symptoms'] * 3)
        # Add name words too
        symptoms_text += ' ' + cond['name'].lower().replace(' ', '_')
        condition_symptom_texts[cond_id] = symptoms_text

    cond_ids = list(condition_symptom_texts.keys())
    cond_texts = [condition_symptom_texts[c] for c in cond_ids]

    vectorizer = TfidfVectorizer(ngram_range=(1, 1), analyzer='word')
    cond_vectors = vectorizer.fit_transform(cond_texts)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({
            'vectorizer': vectorizer,
            'cond_vectors': cond_vectors,
            'cond_ids': cond_ids,
        }, f)

    return vectorizer, cond_vectors, cond_ids


def load_symptom_model():
    with open(MODEL_PATH, 'rb') as f:
        data = pickle.load(f)
    return data['vectorizer'], data['cond_vectors'], data['cond_ids']


def model_exists():
    return os.path.exists(MODEL_PATH)


def analyze_symptoms(selected_symptoms: list) -> dict:
    """
    Main analysis function.
    Takes list of symptom keys, returns ranked conditions with scores.
    """
    if not selected_symptoms:
        return {"error": "No symptoms selected"}

    # Ensure model is trained
    if not model_exists():
        train_symptom_model()

    vectorizer, cond_vectors, cond_ids = load_symptom_model()
    from sklearn.metrics.pairwise import cosine_similarity

    # Build symptom query text
    query_text = ' '.join(selected_symptoms)
    query_vec = vectorizer.transform([query_text])

    # Cosine similarity against all conditions
    sims = cosine_similarity(query_vec, cond_vectors).flatten()

    # Also compute direct symptom overlap score
    results = []
    for i, cond_id in enumerate(cond_ids):
        cond = CONDITIONS[cond_id]
        key_syms = set(cond['key_symptoms'])
        selected_set = set(selected_symptoms)

        overlap = len(key_syms & selected_set)
        overlap_pct = overlap / len(key_syms) if key_syms else 0
        tfidf_score = float(sims[i])

        # Combined score: 60% symptom overlap + 40% TF-IDF
        combined = (overlap_pct * 0.6) + (tfidf_score * 0.4)

        if combined > 0.05 or overlap >= 1:
            results.append({
                'condition_id': cond_id,
                'condition': cond,
                'score': combined,
                'overlap': overlap,
                'overlap_pct': overlap_pct,
                'matched_symptoms': list(key_syms & selected_set),
                'missing_symptoms': list(key_syms - selected_set)[:3],
                'probability': min(int(combined * 120), 92),  # Cap at 92%
            })

    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    top_results = results[:5]

    # Check red flag combinations
    red_flags = check_red_flags(selected_symptoms)

    # Determine overall urgency
    overall_urgency = determine_urgency(top_results, red_flags)

    # Get unique specialists needed
    specialists = list(set([r['condition']['specialist'] for r in top_results[:3]]))

    # Get symptom labels
    symptom_labels = [SYMPTOMS[s]['label'] for s in selected_symptoms if s in SYMPTOMS]

    return {
        'symptoms': selected_symptoms,
        'symptom_labels': symptom_labels,
        'conditions': top_results,
        'red_flags': red_flags,
        'overall_urgency': overall_urgency,
        'specialists': specialists[:3],
        'total_symptoms': len(selected_symptoms),
    }


def check_red_flags(symptoms: list) -> list:
    """Check for dangerous symptom combinations."""
    triggered = []
    symptom_set = set(symptoms)
    for combo in RED_FLAG_COMBOS:
        required = set(combo['symptoms'])
        if required & symptom_set == required or (
            len(required) == 1 and required & symptom_set
        ):
            triggered.append(combo)
    return triggered


def determine_urgency(results: list, red_flags: list) -> dict:
    """Determine the highest urgency level."""
    if red_flags:
        for rf in red_flags:
            if rf['urgency'] == 'emergency':
                return {
                    'level': 'emergency',
                    'label': '🚨 EMERGENCY — Seek Immediate Care',
                    'color': 'red',
                    'message': 'Your symptoms suggest a potentially life-threatening condition. Call an ambulance or go to the nearest emergency room immediately.',
                    'icon': '🚨'
                }

    if results:
        top_urgency = results[0]['condition']['urgency']
        if top_urgency == 'emergency':
            return {
                'level': 'emergency',
                'label': '🚨 EMERGENCY',
                'color': 'red',
                'message': 'Seek emergency medical care immediately.',
                'icon': '🚨'
            }
        elif top_urgency == 'see_doctor_today':
            return {
                'level': 'urgent',
                'label': '⚠️ See Doctor Today',
                'color': 'orange',
                'message': 'Your symptoms need medical attention today. Visit a doctor or urgent care clinic.',
                'icon': '⚠️'
            }
        elif top_urgency == 'see_doctor_soon':
            return {
                'level': 'soon',
                'label': '📅 See Doctor This Week',
                'color': 'yellow',
                'message': 'Schedule a doctor appointment within the next few days. Your symptoms need professional evaluation.',
                'icon': '📅'
            }

    return {
        'level': 'monitor',
        'label': '🏠 Monitor at Home',
        'color': 'green',
        'message': 'Your symptoms can likely be managed at home with rest and self-care. See a doctor if symptoms worsen.',
        'icon': '🏠'
    }
