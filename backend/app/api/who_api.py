from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.utils.database import (
    SessionLocal,
)

from app.services.who_service import (
    fetch_who_outbreak_news,
)

from app.services.outbreak_risk_service import (
    get_outbreak_severity,
)

from app.models.who_outbreaks import (
    WhoOutbreakReport,
)

router = APIRouter(
    prefix="/api/who",
    tags=["WHO"],
)

# =====================================================
# DB SESSION
# =====================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# =====================================================
# LIVE OUTBREAK FEED
# =====================================================

@router.get("/outbreaks")
def get_who_outbreaks():

    data = fetch_who_outbreak_news()

    for report in data:
        report["severity"] = get_outbreak_severity(
            report["disease"]
        )

    return {

        "source":
            "WHO",

        "count":
            len(data),

        "reports":
            data,
    }

# =====================================================
# HISTORICAL OUTBREAKS
# =====================================================

@router.get("/history")
def get_outbreak_history(

    country_iso2: str | None = Query(
        default=None,
        description="Filter by ISO2 country code",
    ),

    disease: str | None = Query(
        default=None,
        description="Filter by disease",
    ),

    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
    ),

    db: Session = Depends(get_db),
):

    print(
        "🌍 Fetching outbreak history..."
    )

    # -------------------------------------------------
    # BASE QUERY
    # -------------------------------------------------

    query = (
        db.query(
            WhoOutbreakReport
        )
        .order_by(
            WhoOutbreakReport.ingested_at.desc()
        )
    )

    # -------------------------------------------------
    # COUNTRY FILTER
    # -------------------------------------------------

    if country_iso2:

        query = query.filter(

            WhoOutbreakReport.country_iso2
            == country_iso2.upper()
        )

    # -------------------------------------------------
    # DISEASE FILTER
    # -------------------------------------------------

    if disease:

        query = query.filter(

            WhoOutbreakReport.disease
            == disease
        )

    # -------------------------------------------------
    # LIMIT
    # -------------------------------------------------

    rows = query.limit(limit).all()

    print(
        f"📊 Historical outbreaks: "
        f"{len(rows)}"
    )

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------

    return {

        "source":
            "WHO_DB",

        "count":
            len(rows),

        "reports": [

            {

                "id":
                    row.id,

                "title":
                    row.title,

                "disease":
                    row.disease,

                "severity":
                    get_outbreak_severity(
                        row.disease
                    ),

                "country": {

                    "name":
                        row.country_name,

                    "iso2":
                        row.country_iso2,
                },

                "source":
                    row.source,

                "url":
                    row.url,

                "published":
                    row.published_at,

                "ingested_at":
                    row.ingested_at.isoformat()
                    if row.ingested_at
                    else None,
            }

            for row in rows
        ]
    }

# =====================================================
# OUTBREAK COUNTRIES
# =====================================================

@router.get("/countries")
def outbreak_country_summary(
    db: Session = Depends(get_db),
):

    rows = (
        db.query(
            WhoOutbreakReport
        )
        .all()
    )

    summary = {}

    for row in rows:

        iso2 = (
            row.country_iso2
            or "UNKNOWN"
        )

        if iso2 not in summary:

            summary[iso2] = {

                "country_name":
                    row.country_name,

                "country_iso2":
                    iso2,

                "outbreak_count":
                    0,
            }

        summary[iso2][
            "outbreak_count"
        ] += 1

    result = sorted(

        summary.values(),

        key=lambda x:
            x["outbreak_count"],

        reverse=True,
    )

    return {

        "count":
            len(result),

        "countries":
            result,
    }

# =====================================================
# OUTBREAK DISEASE SUMMARY
# =====================================================

@router.get("/diseases")
def outbreak_disease_summary(
    db: Session = Depends(get_db),
):

    rows = (
        db.query(
            WhoOutbreakReport
        )
        .all()
    )

    summary = {}

    for row in rows:

        disease = (
            row.disease
            or "Unknown"
        )

        if disease not in summary:

            summary[disease] = 0

        summary[disease] += 1

    result = [

        {

            "disease":
                disease,

            "count":
                count,
        }

        for disease, count
        in summary.items()
    ]

    result = sorted(

        result,

        key=lambda x:
            x["count"],

        reverse=True,
    )

    return {

        "count":
            len(result),

        "diseases":
            result,
    }