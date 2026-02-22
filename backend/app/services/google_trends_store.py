from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from datetime import datetime, date
from typing import List, Dict
from app.utils.database import engine
from app.models.google_trends import (
    GoogleTrendsTimeseries,
    GoogleTrendsKeyword,
)

Session = sessionmaker(bind=engine)


# ==========================================================
# STORE DATA (USED DURING CSV IMPORT OR LIVE FETCH)
# ==========================================================
def store_trends(keyword_id: int, country_id: int, df) -> None:
    """
    Store Google Trends dataframe into database.
    Prevents duplicate entries by (keyword_id, country_id, date).
    """

    db = Session()

    try:
        for _, row in df.iterrows():

            row_date = row["date"]

            # Ensure Python date type
            if isinstance(row_date, str):
                row_date = datetime.strptime(row_date, "%Y-%m-%d").date()

            exists = (
                db.query(GoogleTrendsTimeseries)
                .filter(
                    and_(
                        GoogleTrendsTimeseries.keyword_id == keyword_id,
                        GoogleTrendsTimeseries.country_id == country_id,
                        GoogleTrendsTimeseries.date == row_date,
                    )
                )
                .first()
            )

            if exists:
                continue

            record = GoogleTrendsTimeseries(
                keyword_id=keyword_id,
                country_id=country_id,
                date=row_date,
                interest_index=int(row["interest_index"]),
                fetched_at=datetime.utcnow(),
            )

            db.add(record)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error storing trends: {e}")
        raise

    finally:
        db.close()


# ==========================================================
# FETCH DATA (USED BY /signal ENDPOINT)
# ==========================================================
def fetch_google_trends(
    disease_id: int,
    country_id: int,
    start_date: str = "",
    end_date: str = "",
) -> List[Dict]:
    """
    Fetch Google Trends data from database for analytics.
    Returns list of {date, value}.
    """

    db = Session()

    try:
        # --------------------------------------------------
        # FIX: Get all keyword IDs for this disease
        # --------------------------------------------------
        keyword_ids = [
            k.id
            for k in db.query(GoogleTrendsKeyword.id)
            .filter(GoogleTrendsKeyword.disease_id == disease_id)
            .all()
        ]

        if not keyword_ids:
            return []

        # --------------------------------------------------
        # Query timeseries using keyword_ids
        # --------------------------------------------------
        query = db.query(GoogleTrendsTimeseries).filter(
            GoogleTrendsTimeseries.keyword_id.in_(keyword_ids),
            GoogleTrendsTimeseries.country_id == country_id,
        )

        # Date filtering
        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(GoogleTrendsTimeseries.date >= start_date_obj)

        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(GoogleTrendsTimeseries.date <= end_date_obj)

        results = query.order_by(GoogleTrendsTimeseries.date.asc()).all()

        return [
            {
                "date": r.date.isoformat(),
                "value": r.interest_index,
            }
            for r in results
        ]

    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []

    finally:
        db.close()