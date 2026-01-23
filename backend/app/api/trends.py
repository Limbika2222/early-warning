from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.google_trends import GoogleTrendsTimeseries

router = APIRouter(prefix="/api/trends", tags=["Google Trends"])

@router.get("/interest-over-time")
def get_interest_over_time(
    keyword_id: int = Query(...),
    country_id: int = Query(...),
):
    db: Session = SessionLocal()

    rows = (
        db.query(GoogleTrendsTimeseries)
        .filter(
            GoogleTrendsTimeseries.keyword_id == keyword_id,
            GoogleTrendsTimeseries.country_id == country_id,
        )
        .order_by(GoogleTrendsTimeseries.date)
        .all()
    )

    return [
        {"date": r.date.isoformat(), "value": r.interest_index}
        for r in rows
    ]
