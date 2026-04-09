from sqlalchemy.orm import Session
from datetime import date
from app.models.alerts import Alert


def generate_alerts(db: Session, risk_results):
    """
    Generate alerts for MEDIUM and HIGH risk diseases.
    """

    alerts = []

    for item in risk_results:
        level = item["risk_level"]

        if level not in ["HIGH", "MEDIUM"]:
            continue

        message = f"{item['disease']} risk is {level}"

        alert = Alert(
            disease=item["disease"],
            message=message,
            alert_level=level,
            date_created=date.today()
        )

        db.add(alert)

        alerts.append({
            "disease": item["disease"],
            "message": message,
            "level": level
        })

    db.commit()
    return alerts