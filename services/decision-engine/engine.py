from datetime import datetime, timezone
from models import DecisionRequest, DecisionResponse, Decision, Priority, Action, RiskLevel


def score_to_level(score: float) -> RiskLevel:
    if score >= 0.90:
        return RiskLevel.critical
    elif score >= 0.70:
        return RiskLevel.high
    elif score >= 0.40:
        return RiskLevel.medium
    else:
        return RiskLevel.low


def is_high_risk(level: RiskLevel) -> bool:
    return level in [RiskLevel.high, RiskLevel.critical]


def decide(request: DecisionRequest) -> DecisionResponse:
    fraud_high = is_high_risk(request.fraud_risk.level)
    churn_high = is_high_risk(request.churn_risk.level)

    if fraud_high and churn_high:
        decision = Decision.investigate
        priority = Priority.critical
        actions = [
            Action(
                type="block_transaction",
                reason="score de fraude alto com padrão de churn — possível conta comprometida"
            ),
            Action(
                type="notify_cs",
                reason="cliente em risco de churn — acionar antes de bloquear"
            ),
        ]
        explanation = (
            f"Cliente com alto risco de fraude ({request.fraud_risk.score:.2f}) "
            f"e alto risco de churn ({request.churn_risk.score:.2f}). "
            "Combinação sugere possível conta comprometida, não cancelamento voluntário. "
            "Prioridade máxima."
        )

    elif fraud_high and not churn_high:
        decision = Decision.block
        priority = Priority.high
        actions = [
            Action(
                type="block_transaction",
                reason="score de fraude alto sem sinal de churn — bloquear transação"
            ),
        ]
        explanation = (
            f"Alto risco de fraude ({request.fraud_risk.score:.2f}) "
            f"com churn sob controle ({request.churn_risk.score:.2f}). "
            "Bloquear transação suspeita."
        )

    elif not fraud_high and churn_high:
        decision = Decision.retain
        priority = Priority.high
        actions = [
            Action(
                type="notify_cs",
                reason="cliente em risco de churn — acionar Customer Success"
            ),
        ]
        explanation = (
            f"Risco de churn alto ({request.churn_risk.score:.2f}) "
            f"sem sinal de fraude ({request.fraud_risk.score:.2f}). "
            "Acionar CS para retenção."
        )

    else:
        decision = Decision.monitor
        priority = Priority.low
        actions = [
            Action(
                type="monitor",
                reason="sem sinais críticos — manter monitoramento padrão"
            ),
        ]
        explanation = (
            f"Fraude ({request.fraud_risk.score:.2f}) e "
            f"churn ({request.churn_risk.score:.2f}) dentro do normal. "
            "Nenhuma ação necessária."
        )

    return DecisionResponse(
        customer_id=request.customer_id,
        decision=decision,
        priority=priority,
        actions=actions,
        explanation=explanation,
        decided_at=datetime.now(timezone.utc),
    )