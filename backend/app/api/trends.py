from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session
from datetime import datetime
from collections import defaultdict

from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    GoogleTrendsUpload,
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
# GET: Interest over time (single keyword)
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
        {"date": r.date.isoformat(), "value": r.interest_index}
        for r in rows
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
    keyword = (
        db.query(GoogleTrendsKeyword)
        .filter(GoogleTrendsKeyword.keyword_text == disease_keyword)
        .first()
    )
    if not keyword:
        raise HTTPException(status_code=400, detail="Unknown disease keyword")

    country = (
        db.query(Country)
        .filter(Country.iso2 == country_iso2)
        .first()
    )
    if not country:
        raise HTTPException(status_code=400, detail="Unknown country")

    contents = await file.read()

    try:
        df = parse_google_trends_csv(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    rows_inserted = 0
    for _, row in df.iterrows():
        db.add(
            GoogleTrendsTimeseries(
                keyword_id=keyword.id,
                country_id=country.id,
                date=row["date"],
                interest_index=int(row["interest_index"]),
                source="google_trends_csv",
                fetched_at=datetime.utcnow(),
            )
        )
        rows_inserted += 1

    # ✅ upload history
    db.add(
        GoogleTrendsUpload(
            keyword_id=keyword.id,
            country_id=country.id,
            rows_inserted=rows_inserted,
            uploaded_at=datetime.utcnow(),
        )
    )

    db.commit()

    return {
        "status": "success",
        "disease_id": keyword.disease_id,
        "rows_inserted": rows_inserted,
        "date_range": {
            "start": df["date"].min().isoformat(),
            "end": df["date"].max().isoformat(),
        },
    }


# ---------------------------------
# GET: Upload history (EVERY upload)
# ---------------------------------
@router.get("/uploads")
def list_upload_history(db: Session = Depends(get_db)):
    uploads = (
        db.query(
            GoogleTrendsUpload.id,
            GoogleTrendsKeyword.keyword_text,
            GoogleTrendsKeyword.disease_id,
            Country.name.label("country"),
            GoogleTrendsUpload.rows_inserted,
            GoogleTrendsUpload.uploaded_at,
        )
        .join(GoogleTrendsKeyword)
        .join(Country)
        .order_by(GoogleTrendsUpload.uploaded_at.desc())
        .all()
    )

    return [
        {
            "id": u.id,
            "keyword": u.keyword_text,
            "disease_id": u.disease_id,
            "country": u.country,
            "rows_inserted": u.rows_inserted,
            "uploaded_at": u.uploaded_at.isoformat(),
        }
        for u in uploads
    ]


# ---------------------------------
# GET: Aggregated disease signal
# ---------------------------------
@router.get("/aggregate")
def aggregate_disease_signal(
    disease_id: int,
    country_id: int,
    db: Session = Depends(get_db),
):
    keywords = (
        db.query(GoogleTrendsKeyword)
        .filter(GoogleTrendsKeyword.disease_id == disease_id)
        .all()
    )

    if not keywords:
        raise HTTPException(status_code=404, detail="No keywords for disease")

    keyword_ids = [k.id for k in keywords]

    rows = (
        db.query(
            GoogleTrendsTimeseries.date,
            GoogleTrendsTimeseries.interest_index,
        )
        .filter(
            GoogleTrendsTimeseries.keyword_id.in_(keyword_ids),
            GoogleTrendsTimeseries.country_id == country_id,
        )
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="No data for aggregation")

    grouped = defaultdict(list)
    for r in rows:
        grouped[r.date.isoformat()].append(r.interest_index)

    return [
        {"date": date, "value": sum(vals) / len(vals)}
        for date, vals in sorted(grouped.items())
    ]
