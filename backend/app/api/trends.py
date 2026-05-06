from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from collections import defaultdict

from app.utils.database import SessionLocal

from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    GoogleTrendsUpload,
    Country,
)

# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/api/trends",
    tags=["trends"],
)

print("✅ trends.py loaded (GLOBAL GEO-AWARE VERSION)")


# =====================================================
# DB dependency
# =====================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================================
# 🌍 GET: Available countries
# =====================================================

@router.get("/countries")
def list_countries(
    db: Session = Depends(get_db),
):
    """
    Returns all supported countries.
    Used by frontend country selector.
    """

    print("🌍 /countries endpoint called")

    countries = (
        db.query(Country)
        .order_by(Country.name.asc())
        .all()
    )

    print(f"🌍 Countries found: {len(countries)}")

    return [
        {
            "id": country.id,
            "name": country.name,
            "iso2": country.iso2,
        }
        for country in countries
    ]


# =====================================================
# 📊 GET: Upload history
# =====================================================

@router.get("/uploads")
def list_upload_history(
    country_iso2: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns Google Trends upload history.

    Optional:
    - filter by country ISO2
    """

    print(
        f"📚 Upload history requested "
        f"(country_iso2={country_iso2})"
    )

    # -------------------------------------------------
    # Base query
    # -------------------------------------------------

    query = (
        db.query(
            GoogleTrendsUpload,
            Country,
        )
        .join(
            Country,
            GoogleTrendsUpload.country_id == Country.id,
        )
    )

    # -------------------------------------------------
    # Optional geo filter
    # -------------------------------------------------

    if country_iso2:

        country = (
            db.query(Country)
            .filter(
                Country.iso2 == country_iso2.upper()
            )
            .first()
        )

        if not country:
            raise HTTPException(
                status_code=404,
                detail="Country not found",
            )

        query = query.filter(
            GoogleTrendsUpload.country_id
            == country.id
        )

    # -------------------------------------------------
    # Fetch uploads
    # -------------------------------------------------

    uploads = (
        query.order_by(
            GoogleTrendsUpload.uploaded_at.desc()
        )
        .all()
    )

    print(f"🔥 BACKEND UPLOADS: {uploads}")

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return [
        {
            "id": upload.GoogleTrendsUpload.id,

            "keyword":
                upload.GoogleTrendsUpload.keywords,

            "country": {
                "id": upload.Country.id,
                "name": upload.Country.name,
                "iso2": upload.Country.iso2,
            },

            "rows_inserted":
                upload.GoogleTrendsUpload.rows_inserted,

            "uploaded_at":
                upload.GoogleTrendsUpload.uploaded_at.isoformat(),
        }
        for upload in uploads
    ]


# =====================================================
# 📈 GET: Aggregated disease signal
# =====================================================

@router.get("/aggregate")
def aggregate_disease_signal(
    disease_id: int,
    country_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """
    Aggregates Google Trends signals
    for a disease within a country.
    """

    print(
        f"[AGGREGATE] "
        f"disease_id={disease_id}, "
        f"country_id={country_id}"
    )

    # -------------------------------------------------
    # Validate country
    # -------------------------------------------------

    country = (
        db.query(Country)
        .filter(Country.id == country_id)
        .first()
    )

    if not country:
        raise HTTPException(
            status_code=404,
            detail="Country not found",
        )

    # -------------------------------------------------
    # Fetch disease keywords
    # -------------------------------------------------

    keywords = (
        db.query(GoogleTrendsKeyword)
        .filter(
            GoogleTrendsKeyword.disease_id
            == disease_id
        )
        .all()
    )

    if not keywords:
        raise HTTPException(
            status_code=404,
            detail="No keywords found for disease",
        )

    keyword_ids = [k.id for k in keywords]

    print(
        f"[AGGREGATE] "
        f"Keywords found: {len(keyword_ids)}"
    )

    # -------------------------------------------------
    # Geo-aware timeseries query
    # -------------------------------------------------

    query = (
        db.query(
            GoogleTrendsTimeseries.date,
            GoogleTrendsTimeseries.interest_index,
        )
        .filter(
            GoogleTrendsTimeseries.keyword_id.in_(
                keyword_ids
            ),

            GoogleTrendsTimeseries.country_id
            == country_id,
        )
    )

    # -------------------------------------------------
    # Optional date filters
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

    rows = query.all()

    # -------------------------------------------------
    # No rows found
    # -------------------------------------------------

    if not rows:

        print(
            "[AGGREGATE] "
            "No rows found"
        )

        raise HTTPException(
            status_code=404,
            detail=(
                "No trend data found for "
                "selected country and disease"
            ),
        )

    print(
        f"[AGGREGATE] "
        f"Rows fetched: {len(rows)}"
    )

    # -------------------------------------------------
    # Aggregate by date
    # -------------------------------------------------

    grouped = defaultdict(list)

    for row in rows:
        grouped[row.date.isoformat()].append(
            row.interest_index
        )

    result = [
        {
            "date": date_key,
            "value": round(
                sum(values) / len(values),
                2,
            ),
        }
        for date_key, values
        in sorted(grouped.items())
    ]

    print(
        f"[AGGREGATE] "
        f"Output points: {len(result)}"
    )

    # -------------------------------------------------
    # Final response
    # -------------------------------------------------

    return {
        "country": {
            "id": country.id,
            "name": country.name,
            "iso2": country.iso2,
        },

        "disease_id": disease_id,

        "points": result,
    }