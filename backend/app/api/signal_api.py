from fastapi import APIRouter, Query
from typing import List, Dict

from app.services.google_trends_store import fetch_google_trends
from app.services.analytics_service import analyze_trends

router = APIRouter(
    prefix="/api",
    tags=["Signal Analytics"],
)


@router.get("/signal")
def get_signal(
    source: str = Query(..., description="Data source: google | twitter | who"),
    disease_id: int = Query(...),
    country_id: int = Query(...),
    start_date: str = Query("", description="YYYY-MM-DD"),
    end_date: str = Query("", description="YYYY-MM-DD"),
):
    """
    Unified analytics endpoint.

    Returns:
    {
        source,
        metrics: {
            signal_index,
            spike_count,
            momentum_percent,
            risk_level
        },
        trend_data: [
            {
                date,
                value,
                ewma,
                ucl,
                is_spike
            }
        ]
    }
    """

    # -------------------------------------------------
    # 1️⃣ Fetch raw trend data
    # -------------------------------------------------
    if source == "google":
        raw_trend_data = fetch_google_trends(
            disease_id=disease_id,
            country_id=country_id,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        raw_trend_data = []

    # -------------------------------------------------
    # 2️⃣ Handle no data
    # -------------------------------------------------
    if not raw_trend_data:
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

    # -------------------------------------------------
    # 3️⃣ Extract values + dates
    # -------------------------------------------------
    values = [float(point["value"]) for point in raw_trend_data]
    dates = [point["date"] for point in raw_trend_data]

    # -------------------------------------------------
    # 4️⃣ Run professional analytics
    # -------------------------------------------------
    analysis = analyze_trends(values, dates)

    # analysis contains:
    # {
    #   trend_data,
    #   signal_index,
    #   spike_count,
    #   momentum_percent,
    #   risk_level
    # }

    # -------------------------------------------------
    # 5️⃣ Return frontend-compatible structure
    # -------------------------------------------------
    return {
        "source": source,
        "metrics": {
            "signal_index": analysis["signal_index"],
            "spike_count": analysis["spike_count"],
            "momentum_percent": analysis["momentum_percent"],
            "risk_level": analysis["risk_level"],
        },
        "trend_data": analysis["trend_data"],
    }