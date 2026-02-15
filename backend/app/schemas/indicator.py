from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class IndicatorBase(BaseModel):
    code: str
    name: str
    category: str
    unit: Optional[str] = None
    description: Optional[str] = None
    update_frequency: Optional[str] = None


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorResponse(IndicatorBase):
    pass


class IndicatorDataPoint(BaseModel):
    date: datetime
    value: float


class IndicatorDataResponse(BaseModel):
    indicator_code: str
    indicator_name: str
    unit: Optional[str]
    data: List[IndicatorDataPoint]
    latest_value: Optional[float]
    change_percent: Optional[float]


class IndicatorListResponse(BaseModel):
    total: int
    items: List[IndicatorBase]


class IndicatorCompareRequest(BaseModel):
    codes: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class TrendAnalysisResponse(BaseModel):
    indicator_code: str
    trend: str
    change_percent: float
    ma_7: Optional[float] = None
    ma_30: Optional[float] = None
    prediction: Optional[dict] = None
