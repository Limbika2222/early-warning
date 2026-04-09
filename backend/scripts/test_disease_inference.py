import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SessionLocal
from app.services.symptom_analysis_service import calculate_symptom_growth
from app.services.disease_inference_service import infer_disease_scores

db = SessionLocal()

symptom_growth = calculate_symptom_growth(db)
disease_risk = infer_disease_scores(symptom_growth)

print("\nDisease Risk Ranking:")
for d in disease_risk:
    print(d["disease"], "| Score:", d["score"], "| Risk:", d["risk_level"])