from datetime import datetime, timezone


def score_to_level(score: float) -> str:
    if score >= 0.90:
        return "critical"
    elif score >= 0.70:
        return "high"
    elif score >= 0.40:
        return "medium"
    else:
        return "low"


def predict(
    customer_id: str,
    tenure: int,
    contract: str,
    monthly_charges: float,
    internet_service: str,
    tech_support: str,
    payment_method: str,
) -> dict:

    score = 0.0
    risk_factors = []

    # Contrato mensal é o maior sinal de churn
    if contract == "Month-to-month":
        if tenure < 12:
            score += 0.55
            risk_factors.append("contrato mensal com menos de 12 meses")
        else:
            score += 0.35
            risk_factors.append("contrato mensal")
    elif contract == "One year":
        score += 0.11
        risk_factors.append("contrato anual")
    else:
        score += 0.03

    # Fiber optic sem suporte técnico é sinal de insatisfação
    if internet_service == "Fiber optic" and tech_support == "No":
        score += 0.15
        risk_factors.append("fibra ótica sem suporte técnico")

    # Cobrança alta aumenta risco
    if monthly_charges > 80:
        score += 0.10
        risk_factors.append(f"cobrança mensal alta (R$ {monthly_charges:.2f})")

    # Pagamento por boleto é sinal de menor engajamento
    if payment_method == "Electronic check":
        score += 0.05
        risk_factors.append("pagamento por cheque eletrônico")

    score = min(round(score, 4), 1.0)
    level = score_to_level(score)

    return {
        "customer_id": customer_id,
        "score": score,
        "level": level,
        "source": "churn-analytics",
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "tenure": tenure,
            "contract": contract,
            "monthly_charges": monthly_charges,
            "top_risk_factors": risk_factors if risk_factors else ["sem sinais críticos"]
        }
    }