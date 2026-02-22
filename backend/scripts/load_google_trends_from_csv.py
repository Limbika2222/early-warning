import pandas as pd
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from pathlib import Path

from app.utils.database import engine
from app.models.google_trends import (
    GoogleTrendsKeyword,
    Country,
    GoogleTrendsTimeseries,
)

# --------------------
# Database session
# --------------------
Session = sessionmaker(bind=engine)


# --------------------
# Project paths (ROBUST VERSION)
# --------------------
def resolve_project_root() -> Path:
    """
    Walk upward from this file until we find
    the 'early-warning-dashboard' directory.
    This avoids fragile .parents[n] assumptions.
    """
    current = Path(__file__).resolve()

    while current.name != "early-warning-dashboard":
        if current.parent == current:
            raise RuntimeError("Could not locate 'early-warning-dashboard' root")
        current = current.parent

    return current


PROJECT_ROOT = resolve_project_root()

DATA_DIR = PROJECT_ROOT / "data" / "raw" / "google_trends_interest"

print("📁 Project root resolved to:", PROJECT_ROOT)
print("📁 Data directory resolved to:", DATA_DIR)


def load_google_trends_csv(
    filename: str,
    keyword_text: str,
    country_iso2: str,
) -> None:
    """
    Load Google Trends 'Interest over time' CSV into the database.
    """

    db = Session()

    try:
        csv_path = DATA_DIR / filename

        print("🔍 Looking for file at:", csv_path)

        if not csv_path.exists():
            print(f"❌ File not found: {csv_path}")
            return

        # --------------------
        # Read & normalize CSV
        # --------------------
        df = pd.read_csv(csv_path, skiprows=1)
        df.columns = ["date", "interest_index"]

        df = df.dropna(subset=["date", "interest_index"])

        # --------------------
        # Resolve foreign keys
        # --------------------
        keyword = (
            db.query(GoogleTrendsKeyword)
            .filter(GoogleTrendsKeyword.keyword_text == keyword_text)
            .first()
        )

        country = (
            db.query(Country)
            .filter(Country.iso2 == country_iso2)
            .first()
        )

        if not keyword or not country:
            print(f"❌ Keyword or country not found: {keyword_text}, {country_iso2}")
            return

        # --------------------
        # Insert time-series
        # --------------------
        inserted = 0
        skipped = 0

        for _, row in df.iterrows():
            date_value = pd.to_datetime(row["date"]).date()

            exists = (
                db.query(GoogleTrendsTimeseries)
                .filter(
                    GoogleTrendsTimeseries.keyword_id == keyword.id,
                    GoogleTrendsTimeseries.country_id == country.id,
                    GoogleTrendsTimeseries.date == date_value,
                )
                .first()
            )

            if exists:
                skipped += 1
                continue

            record = GoogleTrendsTimeseries(
                keyword_id=keyword.id,
                country_id=country.id,
                date=date_value,
                interest_index=int(row["interest_index"]),
                source="google_trends_csv",
                fetched_at=datetime.now(timezone.utc),
            )

            db.add(record)
            inserted += 1

        db.commit()

        print(
            f"✅ Loaded {inserted} rows from {filename} "
            f"(skipped {skipped} duplicates)"
        )

    finally:
        db.close()


# --------------------
# Manual execution
# --------------------
if __name__ == "__main__":
    load_google_trends_csv(
        filename="google_trends_fever_cough_IN.csv",
        keyword_text="fever cough",
        country_iso2="IN",
    )