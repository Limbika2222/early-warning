from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.google_trends import (
    GoogleTrendsKeyword,
    GoogleTrendsTimeseries,
)
from datetime import datetime, date


# -------------------------------------------------
# 🔥 STORE (MULTI-UPLOAD ENABLED)
# -------------------------------------------------
def store_google_trends_data(parsed_rows, keyword_text, country_id, upload_id):
    """
    FINAL VERSION (MULTI-UPLOAD SUPPORT)

    ✔ Always inserts new rows
    ✔ Allows same keyword + date across uploads
    ✔ Uses upload_id to differentiate datasets
    ✔ No overwriting, no skipping
    """

    db: Session = SessionLocal()

    try:
        keyword_text = keyword_text.lower().strip()

        print(f"\n🔥 [STORE] Processing keyword: {keyword_text}")

        # -------------------------------------------------
        # 🔍 Find keyword
        # -------------------------------------------------
        keyword = (
            db.query(GoogleTrendsKeyword)
            .filter(GoogleTrendsKeyword.keyword_text == keyword_text)
            .first()
        )

        if not keyword:
            print(f"[WARNING] Keyword not found: {keyword_text}")
            return 0

        inserted_count = 0

        for row in parsed_rows:
            try:
                if "date" not in row or "interest" not in row:
                    continue

                raw_date = row["date"]

                # -------------------------------------------------
                # ✅ SAFE DATE HANDLING
                # -------------------------------------------------
                if isinstance(raw_date, datetime):
                    date_obj = raw_date.date()
                elif isinstance(raw_date, date):
                    date_obj = raw_date
                elif isinstance(raw_date, str):
                    date_obj = datetime.strptime(raw_date, "%Y-%m-%d").date()
                else:
                    raise ValueError(f"Invalid date type: {type(raw_date)}")

                interest = int(row["interest"])

                # -------------------------------------------------
                # 🔥 ALWAYS INSERT (NO DUPLICATE CHECK)
                # -------------------------------------------------
                ts = GoogleTrendsTimeseries(
                    keyword_id=keyword.id,
                    country_id=country_id,
                    date=date_obj,
                    interest_index=interest,
                    upload_id=upload_id,  # 🔥 KEY FIX
                )

                db.add(ts)
                inserted_count += 1

            except Exception as row_error:
                print(f"[ROW ERROR] {row_error}")
                continue

        db.commit()

        print(f"[RESULT] {keyword_text}: inserted={inserted_count}")

        return inserted_count

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed storing data: {e}")
        return 0

    finally:
        db.close()


# -------------------------------------------------
# Fetch Google Trends data by keyword
# -------------------------------------------------
def fetch_google_trends_by_keyword(
    keyword,
    country_id,
    start_date="",
    end_date="",
):
    db: Session = SessionLocal()

    try:
        keyword = keyword.lower().strip()

        query = (
            db.query(GoogleTrendsTimeseries, GoogleTrendsKeyword)
            .join(
                GoogleTrendsKeyword,
                GoogleTrendsTimeseries.keyword_id == GoogleTrendsKeyword.id,
            )
            .filter(GoogleTrendsKeyword.keyword_text == keyword)
            .filter(GoogleTrendsTimeseries.country_id == country_id)
        )

        if start_date:
            query = query.filter(GoogleTrendsTimeseries.date >= start_date)

        if end_date:
            query = query.filter(GoogleTrendsTimeseries.date <= end_date)

        results = query.order_by(GoogleTrendsTimeseries.date).all()

        return [
            {
                "date": ts.date.strftime("%Y-%m-%d"),
                "value": ts.interest_index,
                "keyword": kw.keyword_text,
            }
            for ts, kw in results
        ]

    finally:
        db.close()


# -------------------------------------------------
# Fetch all keywords for a disease
# -------------------------------------------------
def fetch_keywords_for_disease(disease_id):
    db: Session = SessionLocal()

    try:
        results = (
            db.query(GoogleTrendsKeyword.keyword_text)
            .filter(GoogleTrendsKeyword.disease_id == disease_id)
            .filter(GoogleTrendsKeyword.active == True)
            .all()
        )

        return [r[0].lower().strip() for r in results]

    finally:
        db.close()