from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.utils.database import get_db

from app.models.report import Report

router = APIRouter(

    prefix="/api/reports",

    tags=["Reports"],
)

# =====================================================
# REPORT HISTORY
# =====================================================

@router.get("/history")
def get_report_history(

    db: Session = Depends(get_db)
):

    reports = (

        db.query(Report)

        .order_by(
            Report.generated_at.desc()
        )

        .all()
    )

    return [

        {

            "id":
                report.id,

            "filename":
                report.filename,

            "report_type":
                report.report_type,

            "generated_at":
                report.generated_at,

            "generated_by":
                report.generated_by,

            "file_path":
                report.file_path,
        }

        for report in reports
    ]