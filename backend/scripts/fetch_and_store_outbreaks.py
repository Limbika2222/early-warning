from app.services.who_service import (
    fetch_who_outbreak_news,
)

from app.services.who_store import (
    store_outbreak_reports,
)

# =====================================================
# FETCH + STORE
# =====================================================

def main():

    print(
        "🌍 Fetching outbreak intelligence..."
    )

    reports = (
        fetch_who_outbreak_news()
    )

    print(
        f"📊 Reports fetched: "
        f"{len(reports)}"
    )

    inserted = (
        store_outbreak_reports(
            reports
        )
    )

    print(
        f"✅ Reports stored: "
        f"{inserted}"
    )

# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":

    main()