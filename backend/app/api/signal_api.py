from fastapi import APIRouter, Query
from collections import defaultdict
from typing import Optional

from app.services.google_trends_store import (
    fetch_google_trends_by_keyword,
    fetch_keywords_for_disease,
)
from app.services.analytics_service import analyze_trends

# 🔥 NEW IMPORT (DB-driven ranking)
from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    Disease,
)

router = APIRouter(
    prefix="/api",
    tags=["Signal Analytics"],
)


# ==========================================================
# 🔥 SYMPTOM-LEVEL SIGNAL (UNCHANGED CORE)
# ==========================================================
@router.get("/signal")
def get_signal(
    source: str = Query(...),
    disease_id: int = Query(...),
    country_id: int = Query(...),
    start_date: str = Query(""),
    end_date: str = Query(""),
):
    """
    Returns SYMPTOM-LEVEL signal data (NOT aggregated)
    """

    keywords = fetch_keywords_for_disease(disease_id)

    if not keywords:
        return {
            "source": source,
            "metrics": {
                "signal_index": 0,
                "spike_count": 0,
                "momentum_percent": 0,
                "risk_level": "No Data",
            },
            "trend_data": [],
        }

    trend_data = []
    all_values = []
    all_dates = []

    for keyword in keywords:
        data = fetch_google_trends_by_keyword(
            keyword=keyword,
            country_id=country_id,
            start_date=start_date,
            end_date=end_date,
        )

        if not data:
            continue

        values = [row["value"] for row in data]
        dates = [row["date"] for row in data]

        analysis = analyze_trends(values, dates)

        for point in analysis["trend_data"]:
            trend_data.append(
                {
                    "date": point["date"],
                    "symptom": keyword.lower(),  # 🔥 normalized
                    "interest": point["value"],
                    "ewma": point["ewma"],
                    "ucl": point["ucl"],
                    "is_spike": point["is_spike"],
                }
            )

        all_values.extend(values)
        all_dates.extend(dates)

    # 🔥 Global metrics
    if all_values:
        global_analysis = analyze_trends(all_values, all_dates)
        metrics = {
            "signal_index": global_analysis["signal_index"],
            "spike_count": global_analysis["spike_count"],
            "momentum_percent": global_analysis["momentum_percent"],
            "risk_level": global_analysis["risk_level"],
        }
    else:
        metrics = {
            "signal_index": 0,
            "spike_count": 0,
            "momentum_percent": 0,
            "risk_level": "No Data",
        }

    return {
        "source": source,
        "metrics": metrics,
        "trend_data": trend_data,
    }


# ==========================================================
# 🔥 NEW: DISEASE RANKING (DB-DRIVEN + WEIGHTED)
# ==========================================================
@router.get("/disease-ranking")
def get_disease_ranking(
    country_id: Optional[int] = Query(None),
    start_date: str = Query(""),
    end_date: str = Query(""),
):
    """
    Aggregate symptom signals → disease ranking

    Uses:
    - keyword → disease_id
    - keyword.weight (importance)
    """

    db = SessionLocal()

    try:
        query = (
            db.query(
                GoogleTrendsTimeseries,
                GoogleTrendsKeyword,
                Disease,
            )
            .join(
                GoogleTrendsKeyword,
                GoogleTrendsTimeseries.keyword_id == GoogleTrendsKeyword.id,
            )
            .join(
                Disease,
                GoogleTrendsKeyword.disease_id == Disease.id,
            )
            .filter(GoogleTrendsKeyword.active == True)
        )

        if country_id:
            query = query.filter(
                GoogleTrendsTimeseries.country_id == country_id
            )

        if start_date:
            query = query.filter(
                GoogleTrendsTimeseries.date >= start_date
            )

        if end_date:
            query = query.filter(
                GoogleTrendsTimeseries.date <= end_date
            )

        records = query.all()

        disease_scores = defaultdict(float)

        for ts, keyword, disease in records:
            value = ts.interest_index
            weight = keyword.weight or 1.0

            # 🔥 WEIGHTED SCORING
            disease_scores[disease.name] += value * weight

        result = [
            {
                "name": disease,
                "value": round(score, 2),
                "year": 2024,
            }
            for disease, score in disease_scores.items()
        ]

        return sorted(result, key=lambda x: x["value"], reverse=True)

    finally:
        db.close()