import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SessionLocal
from app.services.symptom_analysis_service import (
    calculate_symptom_growth,
    get_top_trending_symptoms
)

db = SessionLocal()

growth = calculate_symptom_growth(db)

print("\nAll Symptom Growth:")
for symptom, value in growth.items():
    print(symptom, ":", value)

print("\nTop Trending Symptoms:")
top = get_top_trending_symptoms(db)

for item in top:
    print(item["symptom"], ":", item["growth"])