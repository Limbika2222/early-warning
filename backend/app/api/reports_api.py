from fastapi import APIRouter
from fastapi import Depends

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.utils.database import get_db

from app.services.report_generator import (
    generate_weekly_report,
    generate_monthly_report,
    generate_country_report
)

router = APIRouter(

    prefix="/api/reports",

    tags=["Reports"]
)

@router.get("/weekly")
def create_weekly_report(

    db: Session = Depends(get_db)
):

    pdf_path = generate_weekly_report(
        db
    )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename="weekly_report.pdf"
    )

# =====================================================
# MONTHLY REPORT
# =====================================================

@router.get("/monthly")
def create_monthly_report(

    db: Session = Depends(get_db)
):

    pdf_path = generate_monthly_report(
        db
    )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename="monthly_report.pdf"
    )

# =====================================================
# COUNTRY REPORT
# =====================================================

@router.get("/country/{country_name}")
def create_country_report(

    country_name: str,

    db: Session = Depends(get_db)
):

    pdf_path = generate_country_report(

        db,

        country_name
    )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename=f"{country_name}_report.pdf"
    )