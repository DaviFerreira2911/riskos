from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predictor import predict

app = FastAPI(
    title="RiskOS — Fraud Detector",
    description="Serviço de detecção de fraude transacional.",
    version="1.0.0",
)


class FraudRequest(BaseModel):
    customer_id: str
    transaction_id: str
    amount: float
    hour: int
    distance_from_home: float
    transactions_last_24h: int
    different_location: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "fraud-detector"}


@app.post("/risk/fraud")
def fraud_risk(request: FraudRequest):
    try:
        return predict(
            customer_id=request.customer_id,
            transaction_id=request.transaction_id,
            amount=request.amount,
            hour=request.hour,
            distance=request.distance_from_home,
            transactions_24h=request.transactions_last_24h,
            different_location=request.different_location,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))