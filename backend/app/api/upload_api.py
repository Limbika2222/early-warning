from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from collections import defaultdict
import time
from datetime import datetime

from app.services.google_trends_store import store_google_trends_data
from app.services.google_trends_csv_parser import parse_google_trends_csv

from app.utils.database import SessionLocal
from app.models.google_trends import GoogleTrendsUpload, Country

router = APIRouter(tags=["trends"])


# -------------------------------------------------
# 📤 UPLOAD CSV
# -------------------------------------------------
@router.post("/upload-csv")
async def upload_csv(
    country_id: int = Form(...),
    file: UploadFile = File(...),
):
    print("\n🚨🚨🚨 UPLOAD ENDPOINT HIT 🚨🚨🚨")

    # -----------------------------
    # Validate file
    # -----------------------------
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    print("🔥 FILE READ SUCCESSFULLY")

    # -----------------------------
    # Parse CSV
    # -----------------------------
    parsed_data = parse_google_trends_csv(contents)

    if not parsed_data:
        raise HTTPException(status_code=400, detail="No valid data parsed")

    print(f"[DEBUG] Parsed rows: {len(parsed_data)}")

    # -----------------------------
    # Create upload_id
    # -----------------------------
    upload_id = int(time.time() * 1000)
    print(f"🔥 Upload ID: {upload_id}")

    # -----------------------------
    # Group by keyword
    # -----------------------------
    grouped_data = defaultdict(list)

    for row in parsed_data:
        grouped_data[row["keyword"]].append({
            "date": row["date"],
            "interest": row["interest"],
        })

    keywords_list = list(grouped_data.keys())
    print(f"[DEBUG] Keywords found: {keywords_list[:10]}")

    # -----------------------------
    # Store timeseries
    # -----------------------------
    total_rows_inserted = 0

    for keyword, trends in grouped_data.items():
        print(f"[UPLOAD] Processing keyword: {keyword}")

        inserted = store_google_trends_data(
            parsed_rows=trends,
            keyword_text=keyword,
            country_id=country_id,
            upload_id=upload_id,
        )

        total_rows_inserted += inserted or 0

    print(f"✅ [UPLOAD COMPLETE] Total inserted: {total_rows_inserted}")

    # -------------------------------------------------
    # 🔥 SAVE UPLOAD HISTORY (CORRECT)
    # -------------------------------------------------
    db = SessionLocal()

    try:
        keywords_preview = ", ".join(keywords_list[:5])

        upload_record = GoogleTrendsUpload(
            upload_id=upload_id,
            country_id=country_id,
            keywords=keywords_preview,
            rows_inserted=total_rows_inserted,
            uploaded_at=datetime.utcnow(),
        )

        db.add(upload_record)
        db.commit()

        print("✅ Upload history saved successfully")

    except Exception as e:
        db.rollback()
        print("❌ Failed saving upload history:", e)
        raise e

    finally:
        db.close()

    return {
        "status": "success",
        "upload_id": upload_id,
        "keywords_processed": len(grouped_data),
        "rows_inserted": total_rows_inserted,
    }


# -------------------------------------------------
# 📊 GET UPLOAD HISTORY (🔥 FIXED PROPERLY)
# -------------------------------------------------
@router.get("/uploads")
def get_uploads():
    db = SessionLocal()

    try:
        uploads = (
            db.query(GoogleTrendsUpload)
            .order_by(GoogleTrendsUpload.uploaded_at.desc())
            .all()
        )

        result = []

        for u in uploads:
            # get country safely
            country = (
                db.query(Country)
                .filter(Country.id == u.country_id)
                .first()
            )

            result.append({
                "id": u.id,
                "keyword": u.keywords or "N/A",
                "country": country.name if country else "Unknown",
                "rows_inserted": u.rows_inserted or 0,
                "uploaded_at": u.uploaded_at.isoformat()
                if u.uploaded_at else "",
            })

        print("🔥 BACKEND UPLOADS:", result)

        return result

    except Exception as e:
        print("❌ GET uploads error:", e)
        return []

    finally:
        db.close()