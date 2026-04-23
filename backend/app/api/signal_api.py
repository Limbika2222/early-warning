from fastapi import APIRouter, Query
from collections import defaultdict
from typing import Optional
import re

from app.services.google_trends_store import (
    fetch_google_trends_by_keyword,
    fetch_keywords_for_disease,
)
from app.services.analytics_service import analyze_trends

from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    Disease,
)

router = APIRouter(tags=["Signal Analytics"])


# ==========================================================
# 🔥 CLEAN KEYWORD (FINAL VERSION)
# ==========================================================
def normalize_keyword(keyword: str) -> str:
    if not keyword:
        return ""

    keyword = keyword.lower().strip()

    # 🔥 REMOVE DUPLICATES (.1, .2, etc)
    keyword = re.sub(r"\.\d+$", "", keyword)

    # remove noise
    keyword = keyword.replace("-", " ")
    keyword = keyword.replace("_", " ")

    keyword = keyword.replace("symptoms of", "")
    keyword = keyword.replace("symptom of", "")

    keyword = keyword.replace("influenza-like illness", "flu")
    keyword = keyword.replace("covid-19", "covid")

    keyword = re.sub(r"\s+", " ", keyword)

    return keyword.strip()


# ==========================================================
# 🔥 SAFE VALUE EXTRACTION
# ==========================================================
def get_value(row):
    return row.get("value", row.get("interest", 0))


# ==========================================================
# 🔥 SYMPTOM SIGNAL API (FIXED)
# ==========================================================
@router.get("/signal")
def get_signal(
    source: str = Query(...),
    disease_id: int = Query(...),
    country_id: int = Query(...),
    start_date: str = Query(""),
    end_date: str = Query(""),
):
    print("🔥 SIGNAL API CALLED")

    keywords = fetch_keywords_for_disease(disease_id)

    # -------------------------------------------------
    # FALLBACK
    # -------------------------------------------------
    if not keywords:
        print("⚠️ No disease mapping → fallback to ALL keywords")

        db = SessionLocal()
        try:
            keywords = [
                k.keyword_text
                for k in db.query(GoogleTrendsKeyword).all()
            ]
        finally:
            db.close()

    trend_data = []
    all_values = []
    all_dates = []

    # -------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------
    for keyword in keywords:
        clean_keyword = normalize_keyword(keyword)

        # 🔥 SKIP BAD KEYWORDS
        if not clean_keyword or len(clean_keyword) < 2:
            continue

        print(f"👉 RAW: {keyword} → CLEAN: {clean_keyword}")

        data = fetch_google_trends_by_keyword(
            keyword=keyword,
            country_id=country_id,
            start_date=start_date,
            end_date=end_date,
        )

        if not data:
            continue

        values = [get_value(row) for row in data]
        dates = [row["date"] for row in data]

        # 🔥 skip empty series
        if not any(values):
            continue

        analysis = analyze_trends(values, dates)

        for point in analysis["trend_data"]:
            val = point.get("value", 0)

            trend_data.append(
                {
                    "date": point["date"],
                    "symptom": clean_keyword,   # ✅ CRITICAL FIX
                    "value": val,
                    "interest": val,
                    "ewma": point.get("ewma"),
                    "ucl": point.get("ucl"),
                    "is_spike": point.get("is_spike", False),
                }
            )

        all_values.extend(values)
        all_dates.extend(dates)

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------
    if all_values:
        global_analysis = analyze_trends(all_values, all_dates)

        metrics = {
            "signal_index": global_analysis.get("signal_index", 0),
            "spike_count": global_analysis.get("spike_count", 0),
            "momentum_percent": global_analysis.get("momentum_percent", 0),
            "risk_level": global_analysis.get("risk_level", "LOW"),
        }
    else:
        metrics = {
            "signal_index": 0,
            "spike_count": 0,
            "momentum_percent": 0,
            "risk_level": "No Data",
        }

    print(f"✅ Returning {len(trend_data)} points")

    return {
        "source": source,
        "metrics": metrics,
        "trend_data": trend_data,
    }


# ==========================================================
# 🔥 DISEASE RANKING (UNCHANGED)
# ==========================================================
@router.get("/disease-ranking")
def get_disease_ranking(
    country_id: Optional[int] = Query(None),
    start_date: str = Query(""),
    end_date: str = Query(""),
):
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