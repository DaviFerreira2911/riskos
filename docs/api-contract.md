## FraudDetector
POST http://fraud-detector:8001/risk/fraud

Request:
{
  "customer_id": "cust_abc123",
  "transaction_id": "txn_xyz789",
  "amount": 1500.00,
  "currency": "BRL"
}

Response:
{
  "customer_id": "cust_abc123",
  "score": 0.87,
  "level": "high",
  "source": "fraud-detector",
  "evaluated_at": "2026-06-24T14:00:00Z",
  "metadata": {
    "transaction_id": "txn_xyz789",
    "amount": 1500.00,
    "top_risk_factors": ["horário incomum", "localização diferente do padrão", "valor acima da média"]
  }
}

---

## ChurnAnalytics
POST http://churn-analytics:8002/risk/churn

Request:
{
  "customer_id": "cust_abc123"
}

Response:
{
  "customer_id": "cust_abc123",
  "score": 0.72,
  "level": "high",
  "source": "churn-analytics",
  "evaluated_at": "2026-06-24T14:00:00Z",
  "metadata": {
    "days_since_last_login": 18,
    "support_tickets_open": 2,
    "contract_days_remaining": 45,
    "top_risk_factors": ["queda de uso nos últimos 30 dias", "tickets sem resolução", "contrato próximo do vencimento"]
  }
}

---

## DecisionEngine
POST http://decision-engine:8003/decision

Request:
{
  "customer_id": "cust_abc123",
  "fraud_risk": { "score": 0.87, "level": "high", "source": "fraud-detector", "evaluated_at": "2026-06-24T14:00:00Z", "metadata": {} },
  "churn_risk": { "score": 0.72, "level": "high", "source": "churn-analytics", "evaluated_at": "2026-06-24T14:00:00Z", "metadata": {} }
}

Response:
{
  "customer_id": "cust_abc123",
  "decision": "investigate",
  "priority": "critical",
  "actions": [
    { "type": "block_transaction", "reason": "score de fraude alto com padrão de churn" },
    { "type": "notify_cs", "reason": "cliente em risco de churn" }
  ],
  "explanation": "Alto risco de fraude (0.87) e churn (0.72). Possível conta comprometida.",
  "decided_at": "2026-06-24T14:00:01Z"
}

---

## Erro padrão
{
  "error": "customer_not_found",
  "message": "Nenhum cliente encontrado com o ID informado.",
  "status": 404
}

---

## Portas
pipeline-etl     8000
fraud-detector   8001
churn-analytics  8002
decision-engine  8003
dashboard        3000