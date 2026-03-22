# reports/ml_chatbot.py
# TF-IDF + Cosine Similarity ML chatbot — 100% offline

import os
import pickle
import numpy as np
from .chatbot_knowledge import QA_PAIRS

CHATBOT_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'chatbot_tfidf.pkl')


def train_chatbot():
    """Train TF-IDF vectorizer on Q&A knowledge base and save to disk."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    os.makedirs(os.path.dirname(CHATBOT_MODEL_PATH), exist_ok=True)

    questions = [pair[0] for pair in QA_PAIRS]
    answers   = [pair[1] for pair in QA_PAIRS]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),       # unigrams + bigrams
        stop_words='english',
        max_features=5000,
        sublinear_tf=True,
    )
    question_vectors = vectorizer.fit_transform(questions)

    with open(CHATBOT_MODEL_PATH, 'wb') as f:
        pickle.dump({
            'vectorizer': vectorizer,
            'question_vectors': question_vectors,
            'questions': questions,
            'answers': answers,
        }, f)

    print(f"Chatbot trained on {len(questions)} Q&A pairs.")
    return vectorizer, question_vectors, questions, answers


def load_chatbot():
    """Load trained chatbot model from disk."""
    with open(CHATBOT_MODEL_PATH, 'rb') as f:
        data = pickle.load(f)
    return data['vectorizer'], data['question_vectors'], data['questions'], data['answers']


def chatbot_model_exists():
    return os.path.exists(CHATBOT_MODEL_PATH)


def ml_chat_response(message: str, report_context: dict = None) -> str:
    """
    Use TF-IDF cosine similarity to find the best answer from knowledge base.
    Falls back to a helpful generic response if confidence is low.
    """
    from sklearn.metrics.pairwise import cosine_similarity

    # Ensure model is trained
    if not chatbot_model_exists():
        train_chatbot()

    vectorizer, question_vectors, questions, answers = load_chatbot()

    # Handle report context questions
    if report_context and report_context.get('key_findings'):
        msg_lower = message.lower()
        if any(w in msg_lower for w in ['my report', 'my result', 'explain', 'this report', 'what does it mean', 'my test']):
            risk = report_context.get('risk_level', 'unknown')
            abnormal = [f for f in report_context.get('key_findings', []) if f.get('status') != 'normal']
            if abnormal:
                params = ', '.join([f['parameter'] for f in abnormal[:3]])
                return (f"Based on your uploaded report, I found **{len(abnormal)} abnormal parameter(s)**: {params}.\n\n"
                        f"Your overall risk level is **{risk.upper()}**.\n\n"
                        f"Scroll up on the report page to see detailed medications, precautions, and lifestyle advice. "
                        f"Please consult your doctor for proper diagnosis and treatment.")
            else:
                return (f"Great news! Your report shows all parameters within normal range. "
                        f"Risk level is **LOW**. Keep up your healthy lifestyle! "
                        f"Regular checkups are still recommended.")

    # TF-IDF similarity matching first (so medical questions aren't caught by greetings)
    msg_vector = vectorizer.transform([message])
    similarities = cosine_similarity(msg_vector, question_vectors).flatten()
    best_idx = int(np.argmax(similarities))
    best_score = similarities[best_idx]

    # Confidence threshold
    if best_score >= 0.15:
        return answers[best_idx] + "\n\n⚕️ *Always consult a qualified doctor for personalized medical advice.*"

    # Greeting / thanks handling (checked after medical questions)
    msg_lower = message.lower().strip()
    if any(w in msg_lower for w in ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good evening']):
        return ("👋 Hello! I'm **MediBot**, your AI health assistant.\n\n"
                "I can help you:\n"
                "• Understand your medical report results\n"
                "• Explain blood test, thyroid, lipid, kidney values\n"
                "• Answer general health and medication questions\n\n"
                "Ask me anything like *'What does high TSH mean?'* or *'How to reduce cholesterol?'*")

    if any(w in msg_lower for w in ['thank', 'thanks', 'thank you', 'helpful']):
        return "You're welcome! 😊 Stay healthy and consult your doctor for personalized advice. Take care!"

    # Low confidence — generic helpful response
    return (f"I'm not sure about that specific question, but I can help with:\n\n"
            "• **Blood tests** — hemoglobin, WBC, platelets, blood sugar\n"
            "• **Lipid profile** — cholesterol, triglycerides, HDL, LDL\n"
            "• **Thyroid** — TSH, T3, T4, hypothyroidism, hyperthyroidism\n"
            "• **Kidney function** — creatinine, urine protein\n"
            "• **Vitamins** — Vitamin D, B12, iron\n"
            "• **General health** — diabetes, hypertension, anemia\n\n"
            "Try asking: *'What does high TSH mean?'* or *'How to control diabetes?'*\n\n"
            "⚕️ *For specific medical advice, always consult your doctor.*")
