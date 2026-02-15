from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database import Alert
from ..services.data_fetcher import data_fetcher


class AlertService:
    def create_alert(self, db: Session, user_id: int, indicator_code: str, condition: str, threshold: float) -> Alert:
        alert = Alert(
            user_id=user_id,
            indicator_code=indicator_code,
            condition=condition,
            threshold=threshold,
            is_active=True
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    def get_user_alerts(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Alert]:
        return db.query(Alert).filter(Alert.user_id == user_id).offset(skip).limit(limit).all()

    def get_alert(self, db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == user_id).first()

    def update_alert(self, db: Session, alert_id: int, user_id: int, **kwargs) -> Optional[Alert]:
        alert = self.get_alert(db, alert_id, user_id)
        if alert:
            for key, value in kwargs.items():
                if hasattr(alert, key) and value is not None:
                    setattr(alert, key, value)
            db.commit()
            db.refresh(alert)
        return alert

    def delete_alert(self, db: Session, alert_id: int, user_id: int) -> bool:
        alert = self.get_alert(db, alert_id, user_id)
        if alert:
            db.delete(alert)
            db.commit()
            return True
        return False

    def check_alerts(self, db: Session, user_id: int) -> List[dict]:
        alerts = db.query(Alert).filter(Alert.user_id == user_id, Alert.is_active == True).all()
        triggered = []

        for alert in alerts:
            df = data_fetcher.fetch_indicator_data(alert.indicator_code, force_update=True)
            if df.empty:
                continue

            if "value" in df.columns:
                current_value = float(df["value"].iloc[-1])
            else:
                continue

            is_triggered = False
            if alert.condition == "above" and current_value > alert.threshold:
                is_triggered = True
            elif alert.condition == "below" and current_value < alert.threshold:
                is_triggered = True
            elif alert.condition == "equals" and abs(current_value - alert.threshold) < 0.01:
                is_triggered = True

            if is_triggered:
                alert.last_triggered = datetime.utcnow()
                db.commit()
                triggered.append({
                    "alert_id": alert.id,
                    "indicator_code": alert.indicator_code,
                    "condition": alert.condition,
                    "threshold": alert.threshold,
                    "current_value": current_value,
                    "triggered_at": alert.last_triggered
                })

        return triggered


alert_service = AlertService()
