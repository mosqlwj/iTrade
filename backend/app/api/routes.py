from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.models.db_setup import get_db
from app.models.database import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.schemas.indicator import (
    IndicatorResponse, IndicatorListResponse, IndicatorDataResponse,
    IndicatorDataPoint, IndicatorCompareRequest, TrendAnalysisResponse
)
from app.schemas.alert import AlertCreate, AlertResponse, AlertListResponse, AlertUpdate
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token, oauth2_scheme
from app.core.config import settings
from app.services.data_fetcher import data_fetcher
from app.services.indicator_calculator import indicator_calculator
from app.services.alert_service import alert_service

router = APIRouter(prefix="/api", tags=["api"])


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/indicators", response_model=IndicatorListResponse)
def get_indicators(db: Session = Depends(get_db)):
    indicators = data_fetcher.get_available_indicators()
    return {"total": len(indicators), "items": indicators}


@router.get("/indicators/{indicator_code}/data", response_model=IndicatorDataResponse)
def get_indicator_data(indicator_code: str, force_update: bool = False):
    df = data_fetcher.fetch_indicator_data(indicator_code, force_update=force_update)
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Indicator data not found")
    
    indicator_info = next((i for i in data_fetcher.get_available_indicators() if i["code"] == indicator_code), None)
    
    if "date" in df.columns:
        data_points = []
        for _, row in df.iterrows():
            data_points.append(IndicatorDataPoint(
                date=row["date"],
                value=float(row["value"]) if "value" in row else float(row.iloc[1])
            ))
        latest_value = float(df["value"].iloc[0]) if "value" in df.columns else float(df.iloc[0, 1])
        change = indicator_calculator.calculate_change_percent(
            df["value"].tolist() if "value" in df.columns else df.iloc[:, 1].tolist()
        )
    else:
        data_points = []
        for i, row in df.iterrows():
            data_points.append(IndicatorDataPoint(
                date=row.iloc[0],
                value=float(row.iloc[1])
            ))
        latest_value = float(df.iloc[0, 1])
        change = indicator_calculator.calculate_change_percent(df.iloc[:, 1].tolist())
    
    return IndicatorDataResponse(
        indicator_code=indicator_code,
        indicator_name=indicator_info["name"] if indicator_info else indicator_code,
        unit=indicator_info["unit"] if indicator_info else None,
        data=data_points,
        latest_value=latest_value,
        change_percent=change
    )


@router.post("/indicators/compare")
def compare_indicators(request: IndicatorCompareRequest):
    results = indicator_calculator.compare_indicators(request.codes, request.start_date, request.end_date)
    return results


@router.get("/indicators/{indicator_code}/trend", response_model=TrendAnalysisResponse)
def get_indicator_trend(indicator_code: str):
    trend_data = indicator_calculator.get_indicator_trend(indicator_code)
    return TrendAnalysisResponse(
        indicator_code=trend_data["indicator_code"],
        trend=trend_data["trend"],
        change_percent=trend_data["change_percent"],
        ma_7=trend_data["ma_7"],
        ma_30=trend_data["ma_30"],
        prediction=trend_data.get("prediction")
    )


@router.post("/alerts", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return alert_service.create_alert(db, current_user.id, alert.indicator_code, alert.condition, alert.threshold)


@router.get("/alerts", response_model=AlertListResponse)
def get_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 100):
    alerts = alert_service.get_user_alerts(db, current_user.id, skip, limit)
    return {"total": len(alerts), "items": alerts}


@router.get("/alerts/check")
def check_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return alert_service.check_alerts(db, current_user.id)


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert_update: AlertUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = alert_service.get_alert(db, alert_id, current_user.id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    updated = alert_service.update_alert(
        db, alert_id, current_user.id,
        condition=alert_update.condition,
        threshold=alert_update.threshold,
        is_active=alert_update.is_active
    )
    return updated


@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = alert_service.delete_alert(db, alert_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted successfully"}


@router.get("/dashboard/summary")
def get_dashboard_summary():
    indicators = ["gdp", "cpi", "pmi", "ppi", "rate", "erp"]
    summary = []
    for code in indicators:
        df = data_fetcher.fetch_indicator_data(code)
        trend = indicator_calculator.get_indicator_trend(code)
        indicator_info = next((i for i in data_fetcher.get_available_indicators() if i["code"] == code), None)
        
        latest_date = None
        if not df.empty and "date" in df.columns:
            latest_date = df["date"].iloc[0].strftime("%Y-%m-%d") if hasattr(df["date"].iloc[0], 'strftime') else str(df["date"].iloc[0])[:10]
        
        summary.append({
            "code": code,
            "name": indicator_info["name"] if indicator_info else code,
            "value": trend.get("latest_value"),
            "change": trend.get("change_percent"),
            "trend": trend.get("trend"),
            "unit": indicator_info["unit"] if indicator_info else None,
            "latest_date": latest_date
        })
    return summary
