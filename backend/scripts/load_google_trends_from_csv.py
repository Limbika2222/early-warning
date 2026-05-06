import pandas as pd

from sqlalchemy.orm import sessionmaker

from datetime import datetime, timezone
from pathlib import Path
import time

from app.utils.database import engine

from app.models.google_trends import (
    GoogleTrendsKeyword,
    Country,
    GoogleTrendsTimeseries,
    GoogleTrendsUpload,
)

# --------------------
# Database session
# --------------------
Session = sessionmaker(bind=engine)


# =====================================================
# 🔥 ROBUST PROJECT ROOT
# =====================================================
def resolve_project_root() -> Path:

    current = Path(__file__).resolve()

    while current.name != "backend":

        if current.parent == current:
            raise RuntimeError(
                "Could not locate backend root"
            )

        current = current.parent

    return current


BACKEND_ROOT = resolve_project_root()

PROJECT_ROOT = BACKEND_ROOT.parent

DATA_DIR = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "google_trends"
)

print("📁 Backend root:", BACKEND_ROOT)
print("📁 Project root:", PROJECT_ROOT)
print("📁 Data directory:", DATA_DIR)


# =====================================================
# 🔥 CSV LOADER
# =====================================================
def load_google_trends_csv(
    filename: str,
    keyword_text: str,
    country_iso2: str,
) -> None:

    db = Session()

    try:

        csv_path = DATA_DIR / filename

        print(f"\n🔍 Loading file: {csv_path}")

        if not csv_path.exists():
            print(f"❌ File not found: {csv_path}")
            return

        # -------------------------------------------------
        # 🌍 COUNTRY LOOKUP
        # -------------------------------------------------
        country = (
            db.query(Country)
            .filter(
                Country.iso2 == country_iso2.upper()
            )
            .first()
        )

        if not country:
            print(
                f"❌ Country not found: "
                f"{country_iso2}"
            )
            return

        # -------------------------------------------------
        # 🔥 NORMALIZE KEYWORD
        # -------------------------------------------------
        keyword_text = (
            keyword_text
            .strip()
            .lower()
        )

        # -------------------------------------------------
        # 🔍 FIND OR CREATE KEYWORD
        # -------------------------------------------------
        keyword = (
            db.query(GoogleTrendsKeyword)
            .filter(
                GoogleTrendsKeyword.keyword_text
                == keyword_text
            )
            .first()
        )

        if not keyword:

            keyword = GoogleTrendsKeyword(
                keyword_text=keyword_text,
                active=True,
            )

            db.add(keyword)
            db.commit()
            db.refresh(keyword)

            print(
                f"✅ Created keyword: "
                f"{keyword_text}"
            )

        # -------------------------------------------------
        # 📄 READ CSV
        # -------------------------------------------------
        df = pd.read_csv(csv_path, skiprows=1)

        df.columns = [
            "date",
            "interest_index",
        ]

        df = df.dropna(
            subset=[
                "date",
                "interest_index",
            ]
        )

        # -------------------------------------------------
        # 🔥 CREATE UPLOAD RECORD
        # -------------------------------------------------
        upload_id = int(time.time())

        upload = GoogleTrendsUpload(
            upload_id=upload_id,
            country_id=country.id,
            keywords=keyword_text,
            rows_inserted=0,
        )

        db.add(upload)
        db.commit()

        # -------------------------------------------------
        # 🔥 INSERT TIMESERIES
        # -------------------------------------------------
        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                date_value = (
                    pd.to_datetime(
                        row["date"]
                    ).date()
                )

                interest = int(
                    row["interest_index"]
                )

                # -------------------------------------------------
                # DUPLICATE CHECK
                # -------------------------------------------------
                exists = (
                    db.query(
                        GoogleTrendsTimeseries
                    )
                    .filter(
                        GoogleTrendsTimeseries.keyword_id
                        == keyword.id,

                        GoogleTrendsTimeseries.country_id
                        == country.id,

                        GoogleTrendsTimeseries.date
                        == date_value,
                    )
                    .first()
                )

                if exists:
                    skipped += 1
                    continue

                record = (
                    GoogleTrendsTimeseries(
                        keyword_id=keyword.id,

                        country_id=country.id,

                        date=date_value,

                        interest_index=interest,

                        upload_id=upload_id,

                        source="google_trends_csv",

                        fetched_at=datetime.now(
                            timezone.utc
                        ),
                    )
                )

                db.add(record)

                inserted += 1

            except Exception as row_error:
                print(
                    f"⚠️ Row error: "
                    f"{row_error}"
                )

                continue

        # -------------------------------------------------
        # 🔥 UPDATE UPLOAD RECORD
        # -------------------------------------------------
        upload.rows_inserted = inserted

        db.commit()

        print(
            f"✅ Loaded {inserted} rows "
            f"for {country.name} "
            f"(skipped {skipped})"
        )

    except Exception as e:

        db.rollback()

        print(f"❌ Loader error: {e}")

    finally:
        db.close()


# =====================================================
# 🔥 MANUAL EXECUTION
# =====================================================
if __name__ == "__main__":

    load_google_trends_csv(
        filename="symptoms_group1.csv",

        keyword_text="fever",

        country_iso2="MW",
    )