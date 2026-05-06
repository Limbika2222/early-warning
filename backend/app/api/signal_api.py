from fastapi import (
    APIRouter,
    Query,
    HTTPException,
)

from collections import defaultdict
from typing import Optional

from app.services.google_trends_store import (
    fetch_google_trends_by_keyword,
    fetch_keywords_for_disease,
    get_country_by_iso2,
)

from app.services.analytics_service import (
    analyze_trends,
)

from app.services.symptom_normalizer import (
    normalize_symptom,
)

from app.utils.database import SessionLocal

from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    Disease,
    Country,
)

# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    tags=["Signal Analytics"]
)

# ==========================================================
# SAFE VALUE EXTRACTION
# ==========================================================

def get_value(row):

    return row.get(
        "value",
        row.get("interest", 0)
    )

# ==========================================================
# SIGNAL API
# ==========================================================

@router.get("/signal")
def get_signal(

    source: str = Query(...),

    disease_id: int = Query(...),

    # 🌍 OPTIONAL
    country_iso2: Optional[str] = Query(
        default=None
    ),

    start_date: str = Query(""),

    end_date: str = Query(""),
):
    print("🔥 SIGNAL API CALLED")

    # -------------------------------------------------
    # 🌍 COUNTRY RESOLUTION
    # -------------------------------------------------

    country = None
    country_id = None

    # -------------------------------------------------
    # GLOBAL MODE
    # -------------------------------------------------

    if (
        country_iso2
        and country_iso2.upper()
        != "GLOBAL"
    ):

        country = get_country_by_iso2(
            country_iso2
        )

        if not country:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Country not found: "
                    f"{country_iso2}"
                ),
            )

        country_id = country.id

        print(
            f"🌍 Country resolved: "
            f"{country.name} "
            f"({country.iso2}) "
            f"→ id={country_id}"
        )

    else:

        print(
            "🌍 GLOBAL MODE ENABLED"
        )

    # -------------------------------------------------
    # FETCH KEYWORDS
    # -------------------------------------------------

    keywords = (
        fetch_keywords_for_disease(
            disease_id
        )
    )

    # -------------------------------------------------
    # FALLBACK
    # -------------------------------------------------

    if not keywords:

        print(
            "⚠️ No disease mapping "
            "→ fallback to ALL keywords"
        )

        db = SessionLocal()

        try:

            keywords = [
                k.keyword_text
                for k in (
                    db.query(
                        GoogleTrendsKeyword
                    ).all()
                )
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

        normalized = normalize_symptom(
            keyword
        )

        # skip junk
        if (
            not normalized
            or len(normalized) < 2
        ):
            continue

        print(
            f"👉 RAW: {keyword} "
            f"→ NORMALIZED: "
            f"{normalized}"
        )

        # -------------------------------------------------
        # FETCH GEO-AWARE DATA
        # -------------------------------------------------

        data = (
            fetch_google_trends_by_keyword(
                keyword=keyword,

                # 🔥 GLOBAL SUPPORT
                country_id=country_id,

                start_date=start_date,

                end_date=end_date,
            )
        )

        if not data:
            continue

        values = [
            get_value(row)
            for row in data
        ]

        dates = [
            row["date"]
            for row in data
        ]

        # skip empty series
        if not any(values):
            continue

        analysis = analyze_trends(
            values,
            dates,
        )

        for point in (
            analysis["trend_data"]
        ):

            val = point.get(
                "value",
                0,
            )

            trend_data.append({
                "date":
                    point["date"],

                "symptom":
                    normalized,

                "value":
                    val,

                "interest":
                    val,

                "ewma":
                    point.get("ewma"),

                "ucl":
                    point.get("ucl"),

                "is_spike":
                    point.get(
                        "is_spike",
                        False,
                    ),
            })

        all_values.extend(values)

        all_dates.extend(dates)

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------

    if all_values:

        global_analysis = (
            analyze_trends(
                all_values,
                all_dates,
            )
        )

        metrics = {

            "signal_index":
                global_analysis.get(
                    "signal_index",
                    0,
                ),

            "spike_count":
                global_analysis.get(
                    "spike_count",
                    0,
                ),

            "momentum_percent":
                global_analysis.get(
                    "momentum_percent",
                    0,
                ),

            "risk_level":
                global_analysis.get(
                    "risk_level",
                    "LOW",
                ),
        }

    else:

        metrics = {
            "signal_index": 0,
            "spike_count": 0,
            "momentum_percent": 0,
            "risk_level": "No Data",
        }

    print(
        f"✅ Returning "
        f"{len(trend_data)} points"
    )

    # -------------------------------------------------
    # COUNTRY RESPONSE
    # -------------------------------------------------

    country_response = None

    if country:

        country_response = {
            "id": country.id,
            "name": country.name,
            "iso2": country.iso2,
        }

    else:

        country_response = {
            "id": None,
            "name": "Global",
            "iso2": "GLOBAL",
        }

    # -------------------------------------------------
    # FINAL RESPONSE
    # -------------------------------------------------

    return {
        "source": source,

        "country": country_response,

        "metrics": metrics,

        "trend_data": trend_data,
    }

# ==========================================================
# DISEASE RANKING
# ==========================================================

@router.get("/disease-ranking")
def get_disease_ranking(

    country_iso2: Optional[str] = Query(
        None
    ),

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
                GoogleTrendsTimeseries.keyword_id
                == GoogleTrendsKeyword.id,
            )
            .join(
                Disease,
                GoogleTrendsKeyword.disease_id
                == Disease.id,
            )
            .filter(
                GoogleTrendsKeyword.active
                == True
            )
        )

        # -------------------------------------------------
        # COUNTRY FILTER
        # -------------------------------------------------

        if (
            country_iso2
            and country_iso2.upper()
            != "GLOBAL"
        ):

            country = get_country_by_iso2(
                country_iso2
            )

            if not country:

                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Country not found: "
                        f"{country_iso2}"
                    ),
                )

            query = query.filter(
                GoogleTrendsTimeseries.country_id
                == country.id
            )

        # -------------------------------------------------
        # DATE FILTERS
        # -------------------------------------------------

        if start_date:

            query = query.filter(
                GoogleTrendsTimeseries.date
                >= start_date
            )

        if end_date:

            query = query.filter(
                GoogleTrendsTimeseries.date
                <= end_date
            )

        records = query.all()

        disease_scores = defaultdict(float)

        for ts, keyword, disease in records:

            value = ts.interest_index

            weight = (
                keyword.weight or 1.0
            )

            disease_scores[
                disease.name
            ] += (
                value * weight
            )

        result = [
            {
                "name": disease,
                "value": round(score, 2),
                "year": 2024,
            }
            for disease, score
            in disease_scores.items()
        ]

        return sorted(
            result,
            key=lambda x: x["value"],
            reverse=True,
        )

    finally:

        db.close()