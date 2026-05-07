from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from datetime import datetime

from app.utils.database import Base

# =====================================================
# WHO / OFFICIAL OUTBREAK REPORTS
# =====================================================

class WhoOutbreakReport(Base):

    __tablename__ = "who_outbreak_reports"

    # -------------------------------------------------
    # PRIMARY KEY
    # -------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # -------------------------------------------------
    # OUTBREAK DATA
    # -------------------------------------------------

    title = Column(
        String,
        nullable=False,
    )

    disease = Column(
        String,
        nullable=False,
        default="Unknown",
    )

    # -------------------------------------------------
    # GEO
    # -------------------------------------------------

    country_name = Column(
        String,
        nullable=True,
    )

    country_iso2 = Column(
        String,
        nullable=True,
        index=True,
    )

    # -------------------------------------------------
    # SOURCE
    # -------------------------------------------------

    source = Column(
        String,
        nullable=True,
    )

    url = Column(
        String,
        unique=True,
        nullable=False,
    )

    # -------------------------------------------------
    # TIMESTAMPS
    # -------------------------------------------------

    published_at = Column(
        String,
        nullable=True,
    )

    ingested_at = Column(
        DateTime,
        default=datetime.utcnow,
    )