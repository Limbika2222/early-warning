from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional

from app.services.reddit_service import RedditService
from app.services.reddit_filter_service import RedditFilterService
from app.services.symptom_extraction_service import SymptomExtractionService
from app.services.time_series_service import TimeSeriesService
from app.services.ewma_service import EWMASignalService
from app.services.disease_detection_service import DiseaseDetectionService

router = APIRouter()

# -------------------------------------------------
# 🔥 GLOBAL ALERT HISTORY (PERSIST IN MEMORY)
# -------------------------------------------------
alert_history = []


# ❗ ROUTE (final = /api/reddit/signal)
@router.get("/reddit/signal")
def get_reddit_signal(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):

    # -------------------------------------------------
    # Initialize services
    # -------------------------------------------------
    reddit_service = RedditService()
    filter_service = RedditFilterService()
    extractor = SymptomExtractionService()
    ts_service = TimeSeriesService()
    ewma_service = EWMASignalService()
    disease_service = DiseaseDetectionService()

    # -------------------------------------------------
    # Step 1: Fetch posts
    # -------------------------------------------------
    posts = reddit_service.fetch_health_signals() or []

    # -------------------------------------------------
    # 🔥 NEW: FILTER POSTS BY DATE RANGE
    # -------------------------------------------------
    if start_date or end_date:
        filtered_by_date = []

        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        for post in posts:
            post_date_str = post.get("created_date")

            if not post_date_str:
                continue

            try:
                post_dt = datetime.strptime(post_date_str[:10], "%Y-%m-%d")
            except:
                continue

            if start_dt and post_dt < start_dt:
                continue
            if end_dt and post_dt > end_dt:
                continue

            filtered_by_date.append(post)

        posts = filtered_by_date

    # -------------------------------------------------
    # Step 2: Filter (health relevance)
    # -------------------------------------------------
    filtered_posts = filter_service.filter_posts(posts) or []

    # -------------------------------------------------
    # Step 3: Extract symptoms
    # -------------------------------------------------
    signals = extractor.process_posts(filtered_posts) or []

    # 🔥 FALLBACK (if no data in selected range)
    if len(signals) == 0:
        # use original posts (no date filter)
        fallback_posts = filter_service.filter_posts(
            reddit_service.fetch_health_signals()
        ) or []

        signals = extractor.process_posts(fallback_posts) or []

    # -------------------------------------------------
    # Step 4: Time series (FIXED)
    # -------------------------------------------------
    time_series = ts_service.generate_time_series(signals) or []

    # 🔥 FIX: keep date continuity for EWMA
    flattened = ts_service.fill_missing_dates_per_symptom(time_series)

    # -------------------------------------------------
    # Step 5: Alerts (WITH TIMESTAMP + HISTORY)
    # -------------------------------------------------
    alerts = ewma_service.detect_spikes(flattened) or []

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    for alert in alerts:
        alert["generated_at"] = timestamp

    alert_history.extend(alerts)

    # keep last 50 alerts
    if len(alert_history) > 50:
        del alert_history[:-50]

    # -------------------------------------------------
    # Step 6: DISEASE DETECTION
    # -------------------------------------------------
    probable_diseases = disease_service.detect_diseases(flattened)

    # 🔥 Link alerts to top disease
    if alerts and probable_diseases:
        top_disease = probable_diseases[0]["disease"]
        for alert in alerts:
            alert["likely_disease"] = top_disease

    # -------------------------------------------------
    # Step 7: Metrics
    # -------------------------------------------------
    total_mentions = sum(item.get("count", 0) for item in flattened)

    unique_symptoms = len(
        set(
            item.get("symptom")
            for item in flattened
            if item.get("count", 0) > 0
        )
    )

    symptom_counts = {}
    for item in flattened:
        count = item.get("count", 0)
        symptom = item.get("symptom")

        if count > 0 and symptom:
            symptom_counts[symptom] = (
                symptom_counts.get(symptom, 0) + count
            )

    top_symptom = (
        max(symptom_counts, key=symptom_counts.get)
        if symptom_counts else None
    )

    metrics = {
        "signal_index": total_mentions,
        "active_symptoms": unique_symptoms,
        "alerts": len(alerts),
        "top_symptom": top_symptom,
        "last_updated": timestamp
    }

    # -------------------------------------------------
    # Step 8: Sample posts (STRICT DATE CONSISTENCY)
    # -------------------------------------------------

    # 🔥 sort posts by date (latest first)
    filtered_posts = sorted(
        filtered_posts,
        key=lambda x: x.get("created_date", ""),
        reverse=True
    )

    # 🔥 ensure only correct date range (extra safety)
    if start_date or end_date:
        strict_posts = []

        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        for post in filtered_posts:
            post_date_str = post.get("created_date")

            if not post_date_str:
                continue

            try:
                post_dt = datetime.strptime(post_date_str[:10], "%Y-%m-%d")
            except:
                continue

            if start_dt and post_dt < start_dt:
                continue
            if end_dt and post_dt > end_dt:
                continue

            strict_posts.append(post)

        filtered_posts = strict_posts

    # 🔥 final sample
    sample_posts = filtered_posts[:10]

    # -------------------------------------------------
    # Final response
    # -------------------------------------------------
    return {
        "time_series": flattened,
        "alerts": alerts,
        "alert_history": alert_history,
        "metrics": metrics,
        "posts": sample_posts,
        "probable_diseases": probable_diseases
    }