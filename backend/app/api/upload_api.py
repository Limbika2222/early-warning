from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Query,
)

from collections import defaultdict
import time

from datetime import datetime

from app.services.google_trends_store import (
    store_google_trends_data,
)

from app.services.google_trends_csv_parser import (
    parse_google_trends_csv,
)

from app.utils.database import SessionLocal

from app.models.google_trends import (
    GoogleTrendsUpload,
    Country,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    tags=["trends"]
)

# =====================================================
# UPLOAD CSV
# =====================================================

@router.post("/upload-csv")
async def upload_csv(

    country_id: int = Form(...),

    file: UploadFile = File(...),
):
    print(
        "\n🚨🚨🚨 UPLOAD ENDPOINT HIT 🚨🚨🚨"
    )

    # -------------------------------------------------
    # Validate file
    # -------------------------------------------------

    if not file.filename.endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files allowed",
        )

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Empty file",
        )

    print("🔥 FILE READ SUCCESSFULLY")

    # -------------------------------------------------
    # Parse CSV
    # -------------------------------------------------

    parsed_data = parse_google_trends_csv(
        contents
    )

    if not parsed_data:

        raise HTTPException(
            status_code=400,
            detail="No valid data parsed",
        )

    print(
        f"[DEBUG] Parsed rows: "
        f"{len(parsed_data)}"
    )

    # -------------------------------------------------
    # Validate country
    # -------------------------------------------------

    db = SessionLocal()

    try:

        country = (
            db.query(Country)
            .filter(
                Country.id == country_id
            )
            .first()
        )

        if not country:

            raise HTTPException(
                status_code=404,
                detail="Country not found",
            )

        print(
            f"🌍 Upload country: "
            f"{country.name} "
            f"({country.iso2})"
        )

    finally:

        db.close()

    # -------------------------------------------------
    # Create upload_id
    # -------------------------------------------------

    upload_id = int(time.time() * 1000)

    print(
        f"🔥 Upload ID: {upload_id}"
    )

    # -------------------------------------------------
    # Group by keyword
    # -------------------------------------------------

    grouped_data = defaultdict(list)

    for row in parsed_data:

        grouped_data[
            row["keyword"]
        ].append({
            "date": row["date"],
            "interest": row["interest"],
        })

    keywords_list = list(
        grouped_data.keys()
    )

    print(
        f"[DEBUG] Keywords found: "
        f"{keywords_list[:10]}"
    )

    # -------------------------------------------------
    # Store timeseries
    # -------------------------------------------------

    total_rows_inserted = 0

    for keyword, trends in (
        grouped_data.items()
    ):

        print(
            f"[UPLOAD] Processing keyword: "
            f"{keyword}"
        )

        inserted = (
            store_google_trends_data(
                parsed_rows=trends,
                keyword_text=keyword,
                country_id=country_id,
                upload_id=upload_id,
            )
        )

        total_rows_inserted += (
            inserted or 0
        )

    print(
        f"✅ [UPLOAD COMPLETE] "
        f"Total inserted: "
        f"{total_rows_inserted}"
    )

    # -------------------------------------------------
    # Save upload history
    # -------------------------------------------------

    db = SessionLocal()

    try:

        keywords_preview = ", ".join(
            keywords_list[:5]
        )

        upload_record = (
            GoogleTrendsUpload(
                upload_id=upload_id,

                country_id=country_id,

                keywords=keywords_preview,

                rows_inserted=
                    total_rows_inserted,

                uploaded_at=
                    datetime.utcnow(),
            )
        )

        db.add(upload_record)

        db.commit()

        print(
            "✅ Upload history saved "
            "successfully"
        )

    except Exception as e:

        db.rollback()

        print(
            "❌ Failed saving upload "
            f"history: {e}"
        )

        raise e

    finally:

        db.close()

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return {
        "status": "success",

        "upload_id": upload_id,

        "country": {
            "id": country.id,
            "name": country.name,
            "iso2": country.iso2,
        },

        "keywords_processed":
            len(grouped_data),

        "rows_inserted":
            total_rows_inserted,
    }

# =====================================================
# GET UPLOAD HISTORY
# =====================================================

@router.get("/uploads")
def get_uploads(

    country_iso2: str | None = Query(
        default=None,
        description="Optional ISO2 country filter",
    ),
):
    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Base query
        # -------------------------------------------------

        query = (
            db.query(
                GoogleTrendsUpload,
                Country,
            )
            .join(
                Country,
                GoogleTrendsUpload.country_id
                == Country.id,
            )
        )

        # -------------------------------------------------
        # Optional geo filter
        # -------------------------------------------------

        if country_iso2:

            query = query.filter(
                Country.iso2
                == country_iso2.upper()
            )

        uploads = (
            query
            .order_by(
                GoogleTrendsUpload.uploaded_at
                .desc()
            )
            .all()
        )

        result = []

        for upload, country in uploads:

            result.append({

                "id":
                    upload.id,

                "keyword":
                    upload.keywords or "N/A",

                # 🔥 FIXED SHAPE
                "country": {
                    "id": country.id,
                    "name": country.name,
                    "iso2": country.iso2,
                },

                "rows_inserted":
                    upload.rows_inserted or 0,

                "uploaded_at":
                    (
                        upload.uploaded_at
                        .isoformat()
                        if upload.uploaded_at
                        else ""
                    ),
            })

        print(
            "🔥 BACKEND UPLOADS:",
            result,
        )

        return result

    except Exception as e:

        print(
            "❌ GET uploads error:",
            e,
        )

        return []

    finally:

        db.close()