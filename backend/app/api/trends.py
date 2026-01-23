from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import SessionLocal
from app.models.google_trends import GoogleTrendsTimeseries

router = APIRouter(
    prefix="/api/trends",
    tags=["trends"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/interest-over-time")
def interest_over_time(
    keyword_id: int,
    country_id: int,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(GoogleTrendsTimeseries)
        .filter(
            GoogleTrendsTimeseries.keyword_id == keyword_id,
            GoogleTrendsTimeseries.country_id == country_id,
        )
        .order_by(GoogleTrendsTimeseries.date.asc())
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="No Google Trends data found")

    return [
        {
            "date": row.date.isoformat(),
            "value": row.interest_index,
        }
        for row in rows
    ]
