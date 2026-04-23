from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Float,
    Boolean,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.utils.database import Base


# =====================================================
# Core reference tables
# =====================================================
class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String)

    keywords = relationship("GoogleTrendsKeyword", back_populates="disease")


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    iso2 = Column(String(2), unique=True, nullable=False)
    iso3 = Column(String(3), unique=True, nullable=False)

    timeseries = relationship("GoogleTrendsTimeseries", back_populates="country")
    uploads = relationship("GoogleTrendsUpload", back_populates="country")


# =====================================================
# Keywords (Symptoms → Disease mapping)
# =====================================================
class GoogleTrendsKeyword(Base):
    __tablename__ = "google_trends_keywords"

    id = Column(Integer, primary_key=True)

    # 🔥 links symptom → disease
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=True)

    keyword_text = Column(String, nullable=False, index=True)
    language = Column(String)
    category = Column(String)

    weight = Column(Float, default=1.0)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    disease = relationship("Disease", back_populates="keywords")
    timeseries = relationship("GoogleTrendsTimeseries", back_populates="keyword")


# =====================================================
# Timeseries (MULTI-UPLOAD SUPPORT)
# =====================================================
class GoogleTrendsTimeseries(Base):
    __tablename__ = "google_trends_timeseries"

    id = Column(Integer, primary_key=True)

    keyword_id = Column(Integer, ForeignKey("google_trends_keywords.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    date = Column(Date, nullable=False)
    interest_index = Column(Integer, nullable=False)

    # 🔥 CRITICAL: identifies which upload this data belongs to
    upload_id = Column(BigInteger, index=True, nullable=True)

    source = Column(String, default="google_trends_csv")
    fetched_at = Column(DateTime, default=datetime.utcnow)

    keyword = relationship("GoogleTrendsKeyword", back_populates="timeseries")
    country = relationship("Country", back_populates="timeseries")


# =====================================================
# 🔥 Upload history (FINAL DESIGN)
# =====================================================
class GoogleTrendsUpload(Base):
    __tablename__ = "google_trends_uploads"

    id = Column(Integer, primary_key=True)

    # 🔥 SAME ID used in timeseries
    upload_id = Column(BigInteger, index=True)

    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    # 🔥 stores preview of uploaded keywords
    keywords = Column(String)

    rows_inserted = Column(Integer, nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    country = relationship("Country", back_populates="uploads")


# =====================================================
# Disease Risk (FINAL OUTPUT TABLE)
# =====================================================
class DiseaseRisk(Base):
    __tablename__ = "disease_risk"

    id = Column(Integer, primary_key=True, index=True)

    disease_id = Column(Integer, index=True)
    disease_name = Column(String)

    risk_score = Column(Float)
    risk_level = Column(String)

    date_calculated = Column(Date)

    created_at = Column(DateTime, default=datetime.utcnow)