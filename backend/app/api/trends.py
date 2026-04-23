from fastapi import APIRouter, Depends, HTTPException
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

router = APIRouter(prefix="/api/trends", tags=["trends"])

print("✅ trends.py loaded (UPLOAD HISTORY FIXED)")


# --------------------
# DB dependency
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# 📊 GET: Upload history (🔥 FIXED)
# =====================================================
@router.get("/uploads")
def list_upload_history(db: Session = Depends(get_db)):
    """
    Returns upload history from GoogleTrendsUpload table
    """

    uploads = (
        db.query(GoogleTrendsUpload, Country)
        .join(Country, GoogleTrendsUpload.country_id == Country.id)
        .order_by(GoogleTrendsUpload.uploaded_at.desc())
        .all()
    )

    return [
        {
            "id": u.GoogleTrendsUpload.id,
            "keyword": u.GoogleTrendsUpload.keywords,  # 🔥 FIX
            "country": u.Country.name,
            "rows_inserted": u.GoogleTrendsUpload.rows_inserted,
            "uploaded_at": u.GoogleTrendsUpload.uploaded_at.isoformat(),
        }
        for u in uploads
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
    print(f"[AGGREGATE] disease_id={disease_id}, country_id={country_id}")

    # --------------------
    # Fetch keywords
    # --------------------
    keywords = (
        db.query(GoogleTrendsKeyword)
        .filter(GoogleTrendsKeyword.disease_id == disease_id)
        .all()
    )

    if not keywords:
        raise HTTPException(status_code=404, detail="No keywords found")

    keyword_ids = [k.id for k in keywords]

    # --------------------
    # Fetch timeseries
    # --------------------
    query = (
        db.query(
            GoogleTrendsTimeseries.date,
            GoogleTrendsTimeseries.interest_index,
        )
        .filter(
            GoogleTrendsTimeseries.keyword_id.in_(keyword_ids),
            GoogleTrendsTimeseries.country_id == country_id,
        )
    )

    if start_date:
        query = query.filter(GoogleTrendsTimeseries.date >= start_date)

    if end_date:
        query = query.filter(GoogleTrendsTimeseries.date <= end_date)

    rows = query.all()

    if not rows:
        raise HTTPException(status_code=404, detail="No data found")

    print(f"[AGGREGATE] Rows fetched: {len(rows)}")

    # --------------------
    # Aggregate (average)
    # --------------------
    grouped = defaultdict(list)

    for r in rows:
        grouped[r.date.isoformat()].append(r.interest_index)

    result = [
        {
            "date": d,
            "value": sum(vals) / len(vals),
        }
        for d, vals in sorted(grouped.items())
    ]

    print(f"[AGGREGATE] Output points: {len(result)}")

    return result