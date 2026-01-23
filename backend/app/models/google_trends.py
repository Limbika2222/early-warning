from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

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


class GoogleTrendsKeyword(Base):
    __tablename__ = "google_trends_keywords"
    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    keyword_text = Column(String)
    language = Column(String)
    category = Column(String)  # symptom | disease
    weight = Column(Float, default=1.0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class GoogleTrendsTimeseries(Base):
    __tablename__ = "google_trends_timeseries"
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey("google_trends_keywords.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))
    date = Column(Date)
    interest_index = Column(Integer)
    source = Column(String, default="google_trends")
    fetched_at = Column(DateTime, default=datetime.utcnow)
