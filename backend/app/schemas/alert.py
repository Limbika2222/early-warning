from pydantic import BaseModel
from datetime import datetime


class AlertBase(BaseModel):
    disease: str
    country: str
    source: str

    risk_score: float
    anomaly_score: float

    severity: str

    outbreak_probability: float

    trend_direction: str

    status: str

    message: str | None = None


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True