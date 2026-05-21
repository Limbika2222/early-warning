from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.utils.database import SessionLocal

from app.models.reddit_signal import (
    RedditSignal,
)

from app.services.reddit_service import (
    RedditService,
)

from app.services.reddit_filter_service import (
    RedditFilterService,
)

from app.services.symptom_extraction_service import (
    SymptomExtractionService,
)

from app.services.time_series_service import (
    TimeSeriesService,
)

from app.services.ewma_service import (
    EWMASignalService,
)

from app.services.disease_detection_service import (
    DiseaseDetectionService,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    prefix="/api",
    tags=["Reddit"],
)

# =====================================================
# ALERT HISTORY
# =====================================================

alert_history = []

# =====================================================
# DATABASE
# =====================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =====================================================
# MAIN REDDIT SIGNAL ENDPOINT
# =====================================================

@router.get("/reddit/signal")
def get_reddit_signal(

    start_date: Optional[str] = Query(None),

    end_date: Optional[str] = Query(None),
):

    print(
        "🚀 Reddit signal pipeline started"
    )

    # =================================================
    # SERVICES
    # =================================================

    reddit_service = RedditService()

    filter_service = RedditFilterService()

    extractor = (
        SymptomExtractionService()
    )

    ts_service = TimeSeriesService()

    ewma_service = EWMASignalService()

    disease_service = (
        DiseaseDetectionService()
    )

    # =================================================
    # FETCH POSTS
    # =================================================

    try:

        posts = (
            reddit_service
            .fetch_health_signals()
        ) or []

    except Exception as e:

        print(
            "❌ Reddit fetch error:",
            str(e)
        )

        posts = []

    print(
        f"📥 Reddit posts fetched: "
        f"{len(posts)}"
    )

    # =================================================
    # OPTIONAL DATE FILTER
    # =================================================

    if start_date or end_date:

        filtered_by_date = []

        start_dt = (

            datetime.strptime(
                start_date,
                "%Y-%m-%d",
            )

            if start_date
            else None
        )

        end_dt = (

            datetime.strptime(
                end_date,
                "%Y-%m-%d",
            )

            if end_date
            else None
        )

        for post in posts:

            post_date_str = post.get(
                "created_date"
            )

            if not post_date_str:
                continue

            try:

                post_dt = (
                    datetime.strptime(
                        post_date_str[:10],
                        "%Y-%m-%d",
                    )
                )

            except Exception:
                continue

            if (
                start_dt
                and post_dt < start_dt
            ):
                continue

            if (
                end_dt
                and post_dt > end_dt
            ):
                continue

            filtered_by_date.append(
                post
            )

        posts = filtered_by_date

    # =================================================
    # HEALTH FILTER
    # =================================================

    try:

        filtered_posts = (
            filter_service
            .filter_posts(posts)
        ) or []

    except Exception as e:

        print(
            "❌ Filter error:",
            str(e)
        )

        filtered_posts = []

    print(
        f"🧪 Health posts: "
        f"{len(filtered_posts)}"
    )

    # =================================================
    # SYMPTOM EXTRACTION
    # =================================================

    try:

        signals = (
            extractor
            .process_posts(
                filtered_posts
            )
        ) or []

    except Exception as e:

        print(
            "❌ Extraction error:",
            str(e)
        )

        signals = []

    # =================================================
    # TIME SERIES
    # =================================================

    try:

        time_series = (
            ts_service
            .generate_time_series(
                signals
            )
        ) or []

        flattened = (
            ts_service
            .fill_missing_dates_per_symptom(
                time_series
            )
        )

    except Exception as e:

        print(
            "❌ Time series error:",
            str(e)
        )

        flattened = []

    # =================================================
    # EWMA ALERTS
    # =================================================

    try:

        alerts = (
            ewma_service
            .detect_spikes(
                flattened
            )
        ) or []

    except Exception as e:

        print(
            "❌ EWMA error:",
            str(e)
        )

        alerts = []

    # =================================================
    # TIMESTAMP
    # =================================================

    timestamp = (
        datetime.utcnow()
        .strftime("%Y-%m-%d %H:%M:%S")
    )

    for alert in alerts:

        alert[
            "generated_at"
        ] = timestamp

    alert_history.extend(alerts)

    if len(alert_history) > 50:

        del alert_history[:-50]

    # =================================================
    # DISEASE DETECTION
    # =================================================

    try:

        probable_diseases = (

            disease_service
            .detect_diseases(
                flattened
            )
        )

    except Exception as e:

        print(
            "❌ Disease detection error:",
            str(e)
        )

        probable_diseases = []

    print(
        f"🦠 Diseases detected: "
        f"{len(probable_diseases)}"
    )

    # =================================================
    # STORE DATABASE SIGNALS
    # =================================================

    db: Session = SessionLocal()

    try:

        # ---------------------------------------------
        # CLEAR OLD SIGNALS
        # ---------------------------------------------

        db.query(
            RedditSignal
        ).delete()

        db.commit()

        # ---------------------------------------------
        # INSERT NEW SIGNALS
        # ---------------------------------------------

        for disease_data in (
            probable_diseases
        ):

            disease_name = (
                disease_data.get(
                    "disease",
                    "Unknown",
                )
            )

            score = int(

                disease_data.get(
                    "score",
                    0,
                )
            )

            reddit_signal = (
                RedditSignal(

                    disease=disease_name,

                    subreddit="health",

                    title=(
                        f"{disease_name} "
                        f"signal detected"
                    ),

                    signal_strength=score,
                )
            )

            db.add(
                reddit_signal
            )

        db.commit()

        print(
            f"✅ Reddit signals stored: "
            f"{len(probable_diseases)}"
        )

    except Exception as e:

        print(
            "❌ Reddit DB error:",
            str(e)
        )

        db.rollback()

    finally:

        db.close()

    # =================================================
    # LINK ALERTS TO TOP DISEASE
    # =================================================

    if (
        alerts
        and probable_diseases
    ):

        top_disease = (

            probable_diseases[0]
            .get("disease")
        )

        for alert in alerts:

            alert[
                "likely_disease"
            ] = top_disease

    # =================================================
    # METRICS
    # =================================================

    total_mentions = sum(

        item.get(
            "count",
            0,
        )

        for item in flattened
    )

    unique_symptoms = len(

        set(

            item.get(
                "symptom"
            )

            for item in flattened

            if item.get(
                "count",
                0,
            ) > 0
        )
    )

    symptom_counts = {}

    for item in flattened:

        count = item.get(
            "count",
            0,
        )

        symptom = item.get(
            "symptom"
        )

        if (
            count > 0
            and symptom
        ):

            symptom_counts[
                symptom
            ] = (

                symptom_counts.get(
                    symptom,
                    0,
                )

                + count
            )

    top_symptom = (

        max(
            symptom_counts,
            key=symptom_counts.get,
        )

        if symptom_counts
        else None
    )

    metrics = {

        "signal_index":
            total_mentions,

        "active_symptoms":
            unique_symptoms,

        "alerts":
            len(alerts),

        "top_symptom":
            top_symptom,

        "last_updated":
            timestamp,
    }

    # =================================================
    # SORT POSTS
    # =================================================

    filtered_posts = sorted(

        filtered_posts,

        key=lambda x:
        x.get(
            "created_date",
            "",
        ),

        reverse=True,
    )

    # =================================================
    # SAMPLE POSTS
    # =================================================

    sample_posts = (
        filtered_posts[:10]
    )

    # =================================================
    # DEBUG
    # =================================================

    print(
        "✅ Reddit pipeline completed"
    )

    # =================================================
    # RESPONSE
    # =================================================

    return {

        "time_series":
            flattened,

        "alerts":
            alerts,

        "alert_history":
            alert_history,

        "metrics":
            metrics,

        "posts":
            sample_posts,

        "probable_diseases":
            probable_diseases,
    }