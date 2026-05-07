from sqlalchemy.orm import Session

from app.utils.database import (
    SessionLocal,
)

from app.models.who_outbreaks import (
    WhoOutbreakReport,
)

# =====================================================
# STORE OUTBREAK REPORTS
# =====================================================

def store_outbreak_reports(
    reports
):

    db: Session = SessionLocal()

    inserted = 0

    try:

        for report in reports:

            url = report.get(
                "url"
            )

            if not url:
                continue

            # -------------------------------------------------
            # DEDUPLICATION
            # -------------------------------------------------

            existing = (
                db.query(
                    WhoOutbreakReport
                )
                .filter(
                    WhoOutbreakReport.url
                    == url
                )
                .first()
            )

            if existing:
                continue

            country = report.get(
                "country",
                {}
            )

            outbreak = (
                WhoOutbreakReport(

                    title=
                        report.get(
                            "title"
                        ),

                    disease=
                        report.get(
                            "disease",
                            "Unknown",
                        ),

                    country_name=
                        country.get(
                            "name"
                        ),

                    country_iso2=
                        country.get(
                            "iso2"
                        ),

                    source=
                        report.get(
                            "source"
                        ),

                    url=url,

                    published_at=
                        report.get(
                            "published"
                        ),
                )
            )

            db.add(outbreak)

            inserted += 1

        db.commit()

        print(
            f"✅ Stored outbreak reports: "
            f"{inserted}"
        )

        return inserted

    except Exception as e:

        db.rollback()

        print(
            "❌ Store outbreak error:",
            str(e)
        )

        return 0

    finally:

        db.close()