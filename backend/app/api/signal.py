from fastapi import APIRouter, Query
from typing import List, Dict

# ✅ IMPORTANT: use STORE version, not live pytrends version
from app.services.google_trends_store import fetch_google_trends
from app.services.analytics_service import calculate_metrics

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
    - trend_data
    - calculated metrics
    """

    # =============================
    # Fetch trend data by source
    # =============================
    if source == "google":
        trend_data = fetch_google_trends(
            disease_id=disease_id,
            country_id=country_id,
            start_date=start_date,
            end_date=end_date,
        )

    elif source == "twitter":
        # 🔥 future integration
        trend_data = []

    elif source == "who":
        # 🔥 future integration
        trend_data = []

    else:
        trend_data = []

    # =============================
    # Extract numeric values
    # =============================
    values = [point["value"] for point in trend_data] if trend_data else []

    # =============================
    # Calculate metrics
    # =============================
    metrics = calculate_metrics(values) if values else {
        "signal_index": 0,
        "spike_count": 0,
        "risk_level": "No Data",
    }

    # =============================
    # Response
    # =============================
    return {
        "source": source,
        "metrics": metrics,
        "trend_data": trend_data,
    }