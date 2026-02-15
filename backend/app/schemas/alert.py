from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AlertBase(BaseModel):
    indicator_code: str
    condition: str
    threshold: float


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    condition: Optional[str] = None
    threshold: Optional[float] = None
    is_active: Optional[bool] = None


class AlertResponse(AlertBase):
    id: int
    user_id: int
    is_active: bool
    last_triggered: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    total: int
    items: List[AlertResponse]


class AlertTrigger(BaseModel):
    alert_id: int
    indicator_code: str
    current_value: float
    condition: str
    threshold: float
    triggered_at: datetime
