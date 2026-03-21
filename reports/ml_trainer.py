# reports/ml_trainer.py
# Generates synthetic training data and trains ML models

import os
import json
import pickle
import numpy as np
from .medical_knowledge import PARAMETERS, RISK_RULES

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models')


def generate_synthetic_data(n_samples=5000):
    """
    Generate synthetic patient records based on WHO/NIH medical standards.
    Each record has parameter values and a risk label.
    """
    np.random.seed(42)
    records = []

    param_list = list(PARAMETERS.keys())

    for _ in range(n_samples):
        record = {}
        abnormal_count = 0

        for param, info in PARAMETERS.items():
            low, high = info["normal"]

            # 70% chance normal, 15% chance low, 15% chance high
            rand = np.random.random()
            if rand < 0.70:
                # Normal range
                if high == 0:  # For binary params like urine_glucose
                    value = 0.0
                else:
                    value = np.random.uniform(low + (high - low) * 0.1, high - (high - low) * 0.1)
            elif rand < 0.85:
                # Low (abnormal)
                if low == 0:
                    value = 0.0
                else:
                    value = np.random.uniform(max(0, low * 0.3), low * 0.95)
                abnormal_count += 1
            else:
                # High (abnormal)
                if high == 0:
                    value = np.random.uniform(15, 100)
                else:
                    value = np.random.uniform(high * 1.05, high * 2.0)
                abnormal_count += 1

            record[param] = round(value, 2)

        # Assign risk level based on abnormal count
        if abnormal_count >= RISK_RULES["critical"]:
            record["risk_level"] = 3  # critical
        elif abnormal_count >= RISK_RULES["high"]:
            record["risk_level"] = 2  # high
        elif abnormal_count >= RISK_RULES["medium"]:
            record["risk_level"] = 1  # medium
        else:
            record["risk_level"] = 0  # low

        records.append(record)

    return records


def train_models():
    """Train ML models and save them to disk."""
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    os.makedirs(MODEL_PATH, exist_ok=True)

    print("Generating synthetic training data...")
    records = generate_synthetic_data(5000)

    param_list = list(PARAMETERS.keys())
    X = np.array([[r[p] for p in param_list] for r in records])
    y = np.array([r["risk_level"] for r in records])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)
    rf_acc = accuracy_score(y_test, rf_model.predict(X_test_scaled))
    print(f"Random Forest Accuracy: {rf_acc:.2%}")

    # Save models and metadata
    with open(os.path.join(MODEL_PATH, 'rf_model.pkl'), 'wb') as f:
        pickle.dump(rf_model, f)
    with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
    with open(os.path.join(MODEL_PATH, 'param_list.pkl'), 'wb') as f:
        pickle.dump(param_list, f)
    with open(os.path.join(MODEL_PATH, 'model_info.json'), 'w') as f:
        json.dump({
            "accuracy": rf_acc,
            "n_samples": len(records),
            "n_features": len(param_list),
            "params": param_list,
        }, f)

    print(f"Models saved to {MODEL_PATH}")
    return rf_acc


def load_models():
    """Load trained models from disk."""
    import pickle
    rf_model = pickle.load(open(os.path.join(MODEL_PATH, 'rf_model.pkl'), 'rb'))
    scaler = pickle.load(open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb'))
    param_list = pickle.load(open(os.path.join(MODEL_PATH, 'param_list.pkl'), 'rb'))
    return rf_model, scaler, param_list


def models_exist():
    return os.path.exists(os.path.join(MODEL_PATH, 'rf_model.pkl'))
