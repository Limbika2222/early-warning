from sqlalchemy import (

    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
)

from sqlalchemy.sql import func

from app.utils.database import Base


class Alert(Base):

    __tablename__ = "alerts"

    # =================================================
    # PRIMARY KEY
    # =================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =================================================
    # ALERT INFORMATION
    # =================================================

    disease = Column(
        String,
        nullable=False
    )

    country = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )

    # =================================================
    # SCORES
    # =================================================

    risk_score = Column(
        Float,
        default=0.0
    )

    anomaly_score = Column(
        Float,
        default=0.0
    )

    outbreak_probability = Column(
        Float,
        default=0.0
    )

    # =================================================
    # ALERT DETAILS
    # =================================================

    severity = Column(
        String,
        default="LOW"
    )

    trend_direction = Column(
        String,
        default="stable"
    )

    status = Column(
        String,
        default="active"
    )

    message = Column(
        String,
        nullable=True
    )

    # =================================================
    # SYSTEM
    # =================================================

    resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )