from sqlalchemy.orm import Session

from app.models.who_outbreaks import (
    WhoOutbreakReport,
)

from app.utils.database import (
    SessionLocal,
)

# =====================================================
# STORE OUTBREAK REPORTS
# =====================================================

def store_outbreak_reports(
    reports: list
):

    db: Session = SessionLocal()

    stored = 0

    try:

        for report in reports:

            # -------------------------------------------------
            # PREVENT DUPLICATES
            # -------------------------------------------------

            existing = (
                db.query(
                    WhoOutbreakReport
                )
                .filter(
                    WhoOutbreakReport.url
                    == report["url"]
                )
                .first()
            )

            if existing:
                continue

            outbreak = (
                WhoOutbreakReport(

                    title=report.get(
                        "title"
                    ),

                    disease=report.get(
                        "disease",
                        "Unknown"
                    ),

                    country_name=(
                        report.get(
                            "country",
                            {}
                        ).get(
                            "name"
                        )
                    ),

                    country_iso2=(
                        report.get(
                            "country",
                            {}
                        ).get(
                            "iso2"
                        )
                    ),

                    source=report.get(
                        "source"
                    ),

                    url=report.get(
                        "url"
                    ),

                    published_at=(
                        report.get(
                            "published"
                        )
                    ),
                )
            )

            db.add(outbreak)

            stored += 1

        db.commit()

        print(
            f"✅ Stored outbreak reports: "
            f"{stored}"
        )

        return stored

    except Exception as e:

        db.rollback()

        print(
            "❌ Storage error:",
            str(e)
        )

        return 0

    finally:

        db.close()