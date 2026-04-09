from sqlalchemy.orm import Session
from datetime import date
from collections import defaultdict

from app.models.google_trends import GoogleTrendsTimeseries, GoogleTrendsKeyword
from app.models.symptom_trends import SymptomTrend


def calculate_symptom_growth(db: Session):
    """
    Calculate symptom growth using:
    Growth = avg(last 3 values) − avg(first 3 values)

    Returns:
        {
            "fever": 12.3,
            "cough": 8.1,
            ...
        }
    """

    results = (
        db.query(
            GoogleTrendsKeyword.keyword_text,
            GoogleTrendsTimeseries.date,
            GoogleTrendsTimeseries.interest_index
        )
        .join(GoogleTrendsTimeseries, GoogleTrendsKeyword.id == GoogleTrendsTimeseries.keyword_id)
        .order_by(GoogleTrendsTimeseries.date.asc())
        .all()
    )

    symptom_values = defaultdict(list)

    for keyword, date_val, interest in results:
        symptom_values[keyword].append(interest)

    growth_results = {}

    for symptom, values in symptom_values.items():
        if len(values) >= 6:
            first_avg = sum(values[:3]) / 3
            last_avg = sum(values[-3:]) / 3
            growth = last_avg - first_avg
        elif len(values) > 1:
            growth = values[-1] - values[0]
        else:
            growth = 0

        growth = round(growth, 2)
        growth_results[symptom] = growth

        # Store in DB
        trend = SymptomTrend(
            symptom=symptom,
            growth_value=growth,
            date_calculated=date.today()
        )
        db.add(trend)

    db.commit()

    return growth_results


def get_top_trending_symptoms(db: Session, top_n: int = 5):
    """
    Returns top N symptoms with highest growth.
    """

    results = (
        db.query(SymptomTrend)
        .order_by(SymptomTrend.growth_value.desc())
        .limit(top_n)
        .all()
    )

    return [
        {
            "symptom": r.symptom,
            "interest": r.growth_value   # 🔥 rename growth → interest
        }
        for r in results
    ]