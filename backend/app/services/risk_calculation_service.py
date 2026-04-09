from sqlalchemy.orm import Session
from datetime import date
from app.models.disease_risk import DiseaseRisk

def calculate_risk_levels(db: Session, ranked_diseases):
    results = []

    for disease, score in ranked_diseases:
        if score > 70:
            level = "HIGH"
        elif score > 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        row = DiseaseRisk(
            disease=disease,
            risk_score=score,
            risk_level=level,
            date_calculated=date.today()
        )
        db.add(row)

        results.append({
            "disease": disease,
            "score": score,
            "level": level
        })

    db.commit()
    return results