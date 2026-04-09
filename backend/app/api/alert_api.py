from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.alerts import Alert

router = APIRouter()

@router.get("/")
def get_alerts():
    db: Session = SessionLocal()
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()

    results = []
    for alert in alerts:
        results.append({
            "id": alert.id,
            "disease_id": alert.disease_id,
            "risk_level": alert.risk_level,
            "message": alert.message,
            "created_at": alert.created_at
        })

    db.close()
    return results