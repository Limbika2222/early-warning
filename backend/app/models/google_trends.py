from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Float,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


# =====================================================
# Core reference tables
# =====================================================
class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    iso2 = Column(String(2), unique=True, nullable=False)
    iso3 = Column(String(3), unique=True, nullable=False)


# =====================================================
# Google Trends keyword catalog
# =====================================================
class GoogleTrendsKeyword(Base):
    __tablename__ = "google_trends_keywords"

    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)

    keyword_text = Column(String, nullable=False)
    language = Column(String)
    category = Column(String)  # symptom | disease
    weight = Column(Float, default=1.0)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# Raw Google Trends timeseries
# =====================================================
class GoogleTrendsTimeseries(Base):
    __tablename__ = "google_trends_timeseries"

    id = Column(Integer, primary_key=True)

    keyword_id = Column(
        Integer,
        ForeignKey("google_trends_keywords.id"),
        nullable=False,
    )
    country_id = Column(
        Integer,
        ForeignKey("countries.id"),
        nullable=False,
    )

    date = Column(Date, nullable=False)
    interest_index = Column(Integer, nullable=False)

    source = Column(String, default="google_trends_csv")
    fetched_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# Upload history (OPTION B)
# =====================================================
class GoogleTrendsUpload(Base):
    __tablename__ = "google_trends_uploads"

    id = Column(Integer, primary_key=True)

    keyword_id = Column(
        Integer,
        ForeignKey("google_trends_keywords.id"),
        nullable=False,
    )
    country_id = Column(
        Integer,
        ForeignKey("countries.id"),
        nullable=False,
    )

    rows_inserted = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
