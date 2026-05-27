from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.utils.database import get_db

from app.models.report import Report

import os

router = APIRouter(

    prefix="/api/reports",

    tags=["Reports"],
)

# =====================================================
# DOWNLOAD REPORT
# =====================================================

@router.get("/download/{report_id}")
def download_report(

    report_id: int,

    db: Session = Depends(get_db)
):

    report = (

        db.query(Report)

        .filter(
            Report.id == report_id
        )

        .first()
    )

    if not report:

        raise HTTPException(

            status_code=404,

            detail="Report not found"
        )

    if not os.path.exists(
        report.file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="PDF file missing"
        )

    return FileResponse(

        path=report.file_path,

        media_type="application/pdf",

        filename=report.filename,
    )