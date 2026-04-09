import sys
import os

# -------------------------------------------------
# Add backend directory to Python path
# -------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import engine, Base

# -------------------------------------------------
# Import ALL models so SQLAlchemy can create tables
# -------------------------------------------------
from app.models.google_trends import (
    Disease,
    Country,
    GoogleTrendsKeyword,
    GoogleTrendsTimeseries,
    GoogleTrendsUpload,
)

from app.models.symptom_trends import SymptomTrend
from app.models.disease_risk import DiseaseRisk
from app.models.alerts import Alert

# Later when added:
# from app.models.wikipedia_data import WikipediaData


# -------------------------------------------------
# Initialize Database
# -------------------------------------------------
def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


# -------------------------------------------------
# Run مباشرة
# -------------------------------------------------
if __name__ == "__main__":
    init_db()