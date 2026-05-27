from app.utils.database import SessionLocal

from app.models.alerts import Alert

db = SessionLocal()

alerts = [

    Alert(
        disease="Influenza",
        country="India",
        source="Google Trends",
        risk_score=82.5,
        anomaly_score=91.2,
        outbreak_probability=0.87,
        severity="HIGH",
        trend_direction="upward",
        status="active",
        message="Search spike detected",
        resolved=False,
    ),

    Alert(
        disease="COVID-19",
        country="South Africa",
        source="WHO",
        risk_score=96.1,
        anomaly_score=98.3,
        outbreak_probability=0.97,
        severity="CRITICAL",
        trend_direction="upward",
        status="active",
        message="WHO confirmed outbreak increase",
        resolved=False,
    ),

    Alert(
        disease="Malaria",
        country="Malawi",
        source="AI Prediction",
        risk_score=71.4,
        anomaly_score=73.5,
        outbreak_probability=0.75,
        severity="MEDIUM",
        trend_direction="stable",
        status="monitoring",
        message="Seasonal increase forecast",
        resolved=False,
    ),

    Alert(
        disease="Dengue",
        country="Brazil",
        source="Reddit",
        risk_score=89.7,
        anomaly_score=93.0,
        outbreak_probability=0.91,
        severity="HIGH",
        trend_direction="upward",
        status="active",
        message="Rapid symptom discussion growth",
        resolved=False,
    ),
]

db.add_all(alerts)

db.commit()

db.close()

print("✅ Alerts seeded successfully")