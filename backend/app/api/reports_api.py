from fastapi import APIRouter
from fastapi import Depends

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.utils.database import get_db

from app.services.report_generator import (
    generate_weekly_report
)

router = APIRouter(

    prefix="/api/reports",

    tags=["Reports"]
)

@router.post("/weekly")
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