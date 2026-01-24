from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    Country,
)
from app.services.google_trends_csv_parser import parse_google_trends_csv

router = APIRouter(prefix="/api/trends", tags=["trends"])


# --------------------
# Database dependency
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------
# GET: Interest over time
# ---------------------------------
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


# ---------------------------------
# POST: Upload Google Trends CSV
# ---------------------------------
@router.post("/upload-csv")
async def upload_google_trends_csv(
    file: UploadFile = File(...),
    disease_keyword: str = Form(...),
    country_iso2: str = Form(...),
    db: Session = Depends(get_db),
):
    # Validate disease keyword
    keyword = (
        db.query(GoogleTrendsKeyword)
        .filter(GoogleTrendsKeyword.keyword_text == disease_keyword)
        .first()
    )
    if not keyword:
        raise HTTPException(status_code=400, detail="Unknown disease keyword")

    # Validate country
    country = (
        db.query(Country)
        .filter(Country.iso2 == country_iso2)
        .first()
    )
    if not country:
        raise HTTPException(status_code=400, detail="Unknown country")

    # Read file
    contents = await file.read()

    try:
        df = parse_google_trends_csv(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    inserted = 0

    for _, row in df.iterrows():
        record = GoogleTrendsTimeseries(
            keyword_id=keyword.id,
            country_id=country.id,
            date=row["date"],
            interest_index=int(row["interest_index"]),
            source="google_trends_csv",
            fetched_at=datetime.now(UTC),
        )
        db.add(record)
        inserted += 1

    db.commit()

    return {
        "status": "success",
        "rows_inserted": inserted,
        "date_range": {
            "start": df["date"].min().isoformat(),
            "end": df["date"].max().isoformat(),
        },
    }
