from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.alerts import Alert

router = APIRouter()

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return alerts