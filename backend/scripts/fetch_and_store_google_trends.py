from sqlalchemy.orm import sessionmaker

from app.utils.database import engine
from app.models.google_trends import (
    GoogleTrendsKeyword,
    Country,
)
from app.services.google_trends_service import fetch_google_trends
from app.services.google_trends_store import store_trends

Session = sessionmaker(bind=engine)
db = Session()

# -----------------------------
# CONFIGURATION (SAFE MODE)
# -----------------------------
TEST_MODE = True   # 🔴 Set to False only after successful testing

TEST_KEYWORDS = ["fever cough", "flu"]
TEST_COUNTRIES = ["IN"]


def run_fetch():
    # -----------------------------
    # SELECT KEYWORDS
    # -----------------------------
    if TEST_MODE:
        keywords = (
            db.query(GoogleTrendsKeyword)
            .filter(
                GoogleTrendsKeyword.active.is_(True),
                GoogleTrendsKeyword.keyword_text.in_(TEST_KEYWORDS),
            )
            .all()
        )
        print("⚠ Running in TEST MODE (limited keywords)")
    else:
        keywords = (
            db.query(GoogleTrendsKeyword)
            .filter(GoogleTrendsKeyword.active.is_(True))
            .all()
        )

    # -----------------------------
    # SELECT COUNTRIES
    # -----------------------------
    if TEST_MODE:
        countries = (
            db.query(Country)
            .filter(Country.iso2.in_(TEST_COUNTRIES))
            .all()
        )
        print("⚠ Running in TEST MODE (limited countries)")
    else:
        countries = db.query(Country).all()

    # -----------------------------
    # FETCH LOOP
    # -----------------------------
    for country in countries:
        print(f"\n🌍 Fetching Google Trends for: {country.name} ({country.iso2})")

        for keyword in keywords:
            print(f"  🔍 Keyword: {keyword.keyword_text}")

            df = fetch_google_trends(
                keyword=keyword.keyword_text,
                country_iso2=country.iso2,
            )

            if df is None or df.empty:
                print("    ⚠ No data returned (skipped)")
                continue

            store_trends(
                keyword_id=keyword.id,
                country_id=country.id,
                df=df,
            )

            print(f"    ✅ Stored {len(df)} rows")

    print("\n✅ Google Trends fetch completed")


if __name__ == "__main__":
    run_fetch()
