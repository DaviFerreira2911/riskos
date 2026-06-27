from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Decision(str, Enum):
    investigate = "investigate"
    block = "block"
    retain = "retain"
    monitor = "monitor"


class Priority(str, Enum):
    low = "low"
    high = "high"
    critical = "critical"


class RiskSignal(BaseModel):
    score: float
    level: RiskLevel
    source: str
    evaluated_at: datetime
    metadata: dict = {}


class DecisionRequest(BaseModel):
    customer_id: str
    fraud_risk: RiskSignal
    churn_risk: RiskSignal


class Action(BaseModel):
    type: str
    reason: str


class DecisionResponse(BaseModel):
    customer_id: str
    decision: Decision
    priority: Priority
    actions: list[Action]
    explanation: str
    decided_at: datetime