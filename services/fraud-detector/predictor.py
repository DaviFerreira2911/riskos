import pandas as pd
import joblib
from datetime import datetime, timezone
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "fraud_model.pkl"
FEATURES_PATH = Path(__file__).parent / "models" / "features.pkl"

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)


def score_to_level(score: float) -> str:
    if score >= 0.90:
        return "critical"
    elif score >= 0.70:
        return "high"
    elif score >= 0.40:
        return "medium"
    else:
        return "low"


def predict(customer_id: str, transaction_id: str, amount: float, hour: int, distance: float, transactions_24h: int, different_location: int) -> dict:
    data = pd.DataFrame([{
        "amount": amount,
        "hour": hour,
        "distance_from_home": distance,
        "transactions_last_24h": transactions_24h,
        "different_location": different_location
    }], columns=features)

    probability = float(model.predict_proba(data)[0][1])
    level = score_to_level(probability)

    return {
        "customer_id": customer_id,
        "score": round(probability, 4),
        "level": level,
        "source": "fraud-detector",
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "transaction_id": transaction_id,
            "amount": amount,
            "top_risk_factors": [
                f"valor R$ {amount:.2f}",
                f"hora {hour}h",
                f"distância {distance}km de casa",
                f"{transactions_24h} transações nas últimas 24h",
                "local diferente do habitual" if different_location else "local habitual"
            ]
        }
    }