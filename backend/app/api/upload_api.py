from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from collections import defaultdict
import time

from app.services.google_trends_store import store_google_trends_data
from app.services.google_trends_csv_parser import parse_google_trends_csv

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.post("/upload-csv")
async def upload_csv(
    country_id: int = Form(...),
    file: UploadFile = File(...),
):
    print("\n🚨🚨🚨 UPLOAD ENDPOINT HIT 🚨🚨🚨")

    # -------------------------------------------------
    # Validate file
    # -------------------------------------------------
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    print("🔥 FILE READ SUCCESSFULLY")

    # -------------------------------------------------
    # Parse CSV
    # -------------------------------------------------
    parsed_data = parse_google_trends_csv(contents)

    if not parsed_data:
        raise HTTPException(status_code=400, detail="No valid data parsed")

    print(f"[DEBUG] Parsed rows: {len(parsed_data)}")
    print(f"[DEBUG] Sample: {parsed_data[:5]}")

    # -------------------------------------------------
    # 🔥 CREATE UNIQUE upload_id (CRITICAL FIX)
    # -------------------------------------------------
    upload_id = int(time.time() * 1000)
    print(f"🔥 Upload ID: {upload_id}")

    # -------------------------------------------------
    # Group by keyword
    # -------------------------------------------------
    grouped_data = defaultdict(list)

    for row in parsed_data:
        grouped_data[row["keyword"]].append({
            "date": row["date"],
            "interest": row["interest"],
        })

    print(f"[DEBUG] Keywords found: {list(grouped_data.keys())[:10]}")

    # -------------------------------------------------
    # Store data
    # -------------------------------------------------
    total_rows_inserted = 0

    for keyword, trends in grouped_data.items():
        print(f"[UPLOAD] Processing keyword: {keyword}")

        inserted = store_google_trends_data(
            parsed_rows=trends,
            keyword_text=keyword,
            country_id=country_id,
            upload_id=upload_id,  # 🔥 PASS upload_id
        )

        total_rows_inserted += inserted if inserted else 0

    print(f"✅ [UPLOAD COMPLETE] Total inserted: {total_rows_inserted}")

    return {
        "status": "success",
        "upload_id": upload_id,
        "keywords_processed": len(grouped_data),
        "rows_inserted": total_rows_inserted,
    }