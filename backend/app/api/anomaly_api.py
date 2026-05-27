from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.utils.database import get_db

from app.services.anomaly_detection import (
    run_anomaly_detection
)

router = APIRouter(
    prefix="/api/anomaly",
    tags=["Anomaly Engine"]
)

@router.post("/run")
def run_engine(
    db: Session = Depends(get_db)
):

    run_anomaly_detection(db)

    return {
        "status":
            "Anomaly detection completed"
    }