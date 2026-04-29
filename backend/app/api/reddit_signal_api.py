from fastapi import APIRouter

from app.services.reddit_service import RedditService
from app.services.reddit_filter_service import RedditFilterService
from app.services.symptom_extraction_service import SymptomExtractionService
from app.services.time_series_service import TimeSeriesService
from app.services.ewma_service import EWMASignalService

router = APIRouter()


# ❗ FIXED ROUTE (no /api here)
@router.get("/reddit/signal")
def get_reddit_signal():

    # -------------------------------------------------
    # Initialize services
    # -------------------------------------------------
    reddit_service = RedditService()
    filter_service = RedditFilterService()
    extractor = SymptomExtractionService()
    ts_service = TimeSeriesService()
    ewma_service = EWMASignalService()

    # -------------------------------------------------
    # Step 1: Fetch posts
    # -------------------------------------------------
    posts = reddit_service.fetch_health_signals() or []

    # -------------------------------------------------
    # Step 2: Filter
    # -------------------------------------------------
    filtered_posts = filter_service.filter_posts(posts) or []

    # -------------------------------------------------
    # Step 3: Extract symptoms
    # -------------------------------------------------
    signals = extractor.process_posts(filtered_posts) or []

    # -------------------------------------------------
    # Step 4: Time series
    # -------------------------------------------------
    time_series = ts_service.generate_time_series(signals) or []
    flattened = ts_service.fill_missing_dates_per_symptom(time_series) or []

    # -------------------------------------------------
    # Step 5: Alerts
    # -------------------------------------------------
    alerts = ewma_service.detect_spikes(flattened) or []

    # -------------------------------------------------
    # Step 6: Metrics
    # -------------------------------------------------
    total_mentions = sum(item.get("count", 0) for item in flattened)

    unique_symptoms = len(
        set(item.get("symptom") for item in flattened if item.get("count", 0) > 0)
    )

    # 🔥 Compute top symptom safely
    symptom_counts = {}
    for item in flattened:
        count = item.get("count", 0)
        symptom = item.get("symptom")

        if count > 0 and symptom:
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + count

    top_symptom = max(symptom_counts, key=symptom_counts.get) if symptom_counts else None

    metrics = {
        "signal_index": total_mentions,
        "active_symptoms": unique_symptoms,
        "alerts": len(alerts),
        "top_symptom": top_symptom
    }

    # -------------------------------------------------
    # Step 7: Sample posts (limit for UI)
    # -------------------------------------------------
    sample_posts = filtered_posts[:10]

    # -------------------------------------------------
    # Final response
    # -------------------------------------------------
    return {
        "time_series": flattened,
        "alerts": alerts,
        "metrics": metrics,
        "posts": sample_posts
    }