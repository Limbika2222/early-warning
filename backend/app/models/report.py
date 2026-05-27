from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from datetime import datetime

from app.utils.database import Base


class Report(Base):

    __tablename__ = "reports"

    # =================================================
    # PRIMARY KEY
    # =================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =================================================
    # REPORT INFO
    # =================================================

    filename = Column(
        String,
        nullable=False,
    )

    report_type = Column(
        String,
        default="weekly",
    )

    file_path = Column(
        String,
        nullable=False,
    )

    # =================================================
    # PERIOD
    # =================================================

    period_start = Column(
        String,
        nullable=True,
    )

    period_end = Column(
        String,
        nullable=True,
    )

    # =================================================
    # METADATA
    # =================================================

    generated_by = Column(
        String,
        default="AI Engine",
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow,
    )