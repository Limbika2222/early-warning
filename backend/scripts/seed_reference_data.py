from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.utils.database import engine
from app.models.google_trends import (
    Disease,
    Country,
    GoogleTrendsKeyword,
)

Session = sessionmaker(bind=engine)
db = Session()


def seed_diseases():
    diseases = [
        Disease(name="Influenza", code="ILI"),
        Disease(name="Malaria", code="MAL"),
        Disease(name="Cholera", code="CHOL"),
        Disease(name="Zika", code="ZIKA"),
    ]

    for disease in diseases:
        exists = db.query(Disease).filter(Disease.name == disease.name).first()
        if not exists:
            db.add(disease)

    db.commit()


def seed_countries():
    countries = [
        Country(name="India", iso2="IN", iso3="IND"),
        Country(name="United States", iso2="US", iso3="USA"),
        Country(name="Brazil", iso2="BR", iso3="BRA"),
        Country(name="Malawi", iso2="MW", iso3="MWI"),
        Country(name="Philippines", iso2="PH", iso3="PHL"),
    ]

    for country in countries:
        exists = db.query(Country).filter(Country.iso2 == country.iso2).first()
        if not exists:
            db.add(country)

    db.commit()


def seed_keywords():
    # Map disease name → keyword used in frontend
    keyword_map = {
        "Influenza": "fever cough",
        "Malaria": "malaria",
        "Cholera": "cholera",
        "Zika": "zika",
    }

    for disease_name, keyword_text in keyword_map.items():
        disease = db.query(Disease).filter(Disease.name == disease_name).first()

        if not disease:
            continue

        exists = (
            db.query(GoogleTrendsKeyword)
            .filter(GoogleTrendsKeyword.keyword_text == keyword_text)
            .first()
        )

        if not exists:
            db.add(
                GoogleTrendsKeyword(
                    disease_id=disease.id,
                    keyword_text=keyword_text,
                    language="en",
                    category="disease",
                    weight=1.0,
                    active=True,
                    created_at=datetime.utcnow(),
                )
            )

    db.commit()


if __name__ == "__main__":
    seed_diseases()
    seed_countries()
    seed_keywords()
    print("✅ Diseases, countries, and keywords seeded successfully")