from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predictor import predict

app = FastAPI(
    title="RiskOS — Churn Analytics",
    description="Serviço de previsão de risco de churn.",
    version="1.0.0",
)


class ChurnRequest(BaseModel):
    customer_id: str
    tenure: int
    contract: str
    monthly_charges: float
    internet_service: str
    tech_support: str
    payment_method: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "churn-analytics"}


@app.post("/risk/churn")
def churn_risk(request: ChurnRequest):
    try:
        return predict(
            customer_id=request.customer_id,
            tenure=request.tenure,
            contract=request.contract,
            monthly_charges=request.monthly_charges,
            internet_service=request.internet_service,
            tech_support=request.tech_support,
            payment_method=request.payment_method,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))