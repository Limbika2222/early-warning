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

from sqlalchemy.orm import (
    relationship,
)

from datetime import datetime

from app.utils.database import Base


# =====================================================
# DISEASES
# =====================================================

class Disease(Base):

    __tablename__ = "diseases"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
    )

    code = Column(String)

    keywords = relationship(
        "GoogleTrendsKeyword",
        back_populates="disease",
    )


# =====================================================
# COUNTRIES
# =====================================================

class Country(Base):

    __tablename__ = "countries"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    iso2 = Column(
        String(2),
        unique=True,
        nullable=False,
    )

    iso3 = Column(
        String(3),
        unique=True,
        nullable=False,
    )

    timeseries = relationship(
        "GoogleTrendsTimeseries",
        back_populates="country",
    )

    uploads = relationship(
        "GoogleTrendsUpload",
        back_populates="country",
    )


# =====================================================
# GOOGLE TRENDS KEYWORDS
# =====================================================

class GoogleTrendsKeyword(Base):

    __tablename__ = (
        "google_trends_keywords"
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    # symptom -> disease mapping
    disease_id = Column(
        Integer,
        ForeignKey("diseases.id"),
        nullable=True,
    )

    keyword_text = Column(
        String,
        nullable=False,
        index=True,
    )

    language = Column(String)

    category = Column(String)

    weight = Column(
        Float,
        default=1.0,
    )

    active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    disease = relationship(
        "Disease",
        back_populates="keywords",
    )

    timeseries = relationship(
        "GoogleTrendsTimeseries",
        back_populates="keyword",
    )


# =====================================================
# GOOGLE TRENDS TIMESERIES
# =====================================================

class GoogleTrendsTimeseries(Base):

    __tablename__ = (
        "google_trends_timeseries"
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    keyword_id = Column(
        Integer,
        ForeignKey(
            "google_trends_keywords.id"
        ),
        nullable=False,
    )

    country_id = Column(
        Integer,
        ForeignKey("countries.id"),
        nullable=False,
    )

    date = Column(
        Date,
        nullable=False,
    )

    interest_index = Column(
        Integer,
        nullable=False,
    )

    # identifies upload batch
    upload_id = Column(
        BigInteger,
        index=True,
        nullable=True,
    )

    source = Column(
        String,
        default="google_trends_csv",
    )

    fetched_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    keyword = relationship(
        "GoogleTrendsKeyword",
        back_populates="timeseries",
    )

    country = relationship(
        "Country",
        back_populates="timeseries",
    )


# =====================================================
# UPLOAD HISTORY
# =====================================================

class GoogleTrendsUpload(Base):

    __tablename__ = (
        "google_trends_uploads"
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    upload_id = Column(
        BigInteger,
        index=True,
    )

    country_id = Column(
        Integer,
        ForeignKey("countries.id"),
        nullable=False,
    )

    keywords = Column(String)

    rows_inserted = Column(
        Integer,
        nullable=False,
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    country = relationship(
        "Country",
        back_populates="uploads",
    )


# =====================================================
# DISEASE RISK
# =====================================================

class DiseaseRisk(Base):

    __tablename__ = "disease_risk"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    disease_id = Column(
        Integer,
        index=True,
    )

    disease_name = Column(String)

    risk_score = Column(Float)

    risk_level = Column(String)

    date_calculated = Column(Date)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# =====================================================
# 🔥 COMPATIBILITY ALIAS
# =====================================================
# Required by prediction engine
# so imports like:
#
# from app.models.google_trends import (
#     GoogleTrendsDaily
# )
#
# continue working correctly.
# =====================================================

GoogleTrendsDaily = GoogleTrendsTimeseries