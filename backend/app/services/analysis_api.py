from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db

from app.services.symptom_analysis_service import calculate_symptom_growth
from app.services.disease_inference_service import infer_disease_scores
from app.services.risk_calculation_service import calculate_risk_levels
from app.services.alert_service import generate_alerts

router = APIRouter()

@router.post("/analysis/run")
def run_analysis(db: Session = Depends(get_db)):
    symptom_growth = calculate_symptom_growth(db)
    ranked = infer_disease_scores(symptom_growth)
    risk = calculate_risk_levels(db, ranked)
    alerts = generate_alerts(db, risk)

    return {
        "symptom_growth": symptom_growth,
        "disease_risk": risk,
        "alerts": alerts
    }