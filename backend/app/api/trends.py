from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from typing import Optional
from collections import defaultdict
import pandas as pd
import io

from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
    GoogleTrendsUpload,
    Country,
)

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
# CSV PARSER (Robust Version)
# ---------------------------------
def parse_google_trends_csv(contents: bytes):
    try:
        df = pd.read_csv(io.BytesIO(contents), skiprows=1)

        if df.shape[1] < 2:
            raise ValueError("Invalid column structure")

        # Normalize to 2 columns only
        df = df.iloc[:, 0:2]
        df.columns = ["date", "interest_index"]

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df["interest_index"] = (
            df["interest_index"]
            .astype(str)
            .str.replace("<1", "0")
        )

        df["interest_index"] = pd.to_numeric(
            df["interest_index"],
            errors="coerce"
        )

        df = df.dropna(subset=["date", "interest_index"])

        if df.empty:
            raise ValueError("No valid rows found")

        # Convert to Python date objects
        df["date"] = df["date"].dt.date

        return df

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid Google Trends CSV format",
        )


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
            "date": r.date.isoformat(),
            "value": r.interest_index,
        }
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
    # Validate keyword
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

    contents = await file.read()
    df = parse_google_trends_csv(contents)

    rows_inserted = 0

    try:
        for _, row in df.iterrows():

            exists = (
                db.query(GoogleTrendsTimeseries)
                .filter(
                    and_(
                        GoogleTrendsTimeseries.keyword_id == keyword.id,
                        GoogleTrendsTimeseries.country_id == country.id,
                        GoogleTrendsTimeseries.date == row["date"],
                    )
                )
                .first()
            )

            if exists:
                continue

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

        # Record upload history
        db.add(
            GoogleTrendsUpload(
                keyword_id=keyword.id,
                country_id=country.id,
                rows_inserted=rows_inserted,
                uploaded_at=datetime.utcnow(),
            )
        )

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Duplicate data detected in upload",
        )

    return {
        "status": "success",
        "rows_inserted": rows_inserted,
        "date_range": {
            "start": df["date"].min().isoformat(),
            "end": df["date"].max().isoformat(),
        },
    }


# ---------------------------------
# GET: Upload history
# ---------------------------------
@router.get("/uploads")
def list_upload_history(
    db: Session = Depends(get_db),
):
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
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
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
        raise HTTPException(status_code=404, detail="No data for aggregation")

    grouped = defaultdict(list)

    for r in rows:
        grouped[r.date.isoformat()].append(r.interest_index)

    return [
        {
            "date": d,
            "value": sum(vals) / len(vals),
        }
        for d, vals in sorted(grouped.items())
    ]