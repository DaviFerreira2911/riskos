from fastapi import FastAPI, HTTPException
from models import DecisionRequest, DecisionResponse
from engine import decide

app = FastAPI(
    title="RiskOS — Decision Engine",
    description="Motor de decisão que combina scores de fraude e churn em uma ação.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "decision-engine"}


@app.post("/decision", response_model=DecisionResponse)
def make_decision(request: DecisionRequest):
    try:
        return decide(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))