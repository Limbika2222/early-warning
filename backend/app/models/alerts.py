from sqlalchemy import Column, Integer, String, Date
from app.utils.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String)
    message = Column(String)
    alert_level = Column(String)
    date_created = Column(Date)