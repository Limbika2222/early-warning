from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.utils.database import get_db

# =====================================================
# IMPORT ALERT MODEL
# =====================================================

from app.models.alerts import Alert

from app.schemas.alert import AlertResponse

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(

    prefix="/api/alerts",

    tags=["Alerts & Anomalies"]
)

# =====================================================
# LIVE ALERTS
# =====================================================

@router.get(
    "/live",
    response_model=list[AlertResponse]
)
def get_live_alerts(

    db: Session = Depends(get_db)
):

    alerts = (

        db.query(Alert)

        .filter(
            Alert.resolved == False
        )

        .order_by(
            Alert.created_at.desc()
        )

        .all()
    )

    return alerts

# =====================================================
# ALERT HISTORY
# =====================================================

@router.get(
    "/history",
    response_model=list[AlertResponse]
)
def get_alert_history(

    db: Session = Depends(get_db)
):

    return (

        db.query(Alert)

        .order_by(
            Alert.created_at.desc()
        )

        .all()
    )

# =====================================================
# COUNTRY ALERTS
# =====================================================

@router.get(
    "/country/{country}",
    response_model=list[AlertResponse]
)
def get_country_alerts(

    country: str,

    db: Session = Depends(get_db)
):

    return (

        db.query(Alert)

        .filter(
            Alert.country == country
        )

        .all()
    )

# =====================================================
# DISEASE ALERTS
# =====================================================

@router.get(
    "/disease/{disease}",
    response_model=list[AlertResponse]
)
def get_disease_alerts(

    disease: str,

    db: Session = Depends(get_db)
):

    return (

        db.query(Alert)

        .filter(
            Alert.disease == disease
        )

        .all()
    )