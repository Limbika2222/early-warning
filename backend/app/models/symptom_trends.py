from sqlalchemy import Column, Integer, String, Float, Date
from app.utils.database import Base

class SymptomTrend(Base):
    __tablename__ = "symptom_trends"

    id = Column(Integer, primary_key=True, index=True)
    symptom = Column(String, index=True)
    growth_value = Column(Float)
    date_calculated = Column(Date)