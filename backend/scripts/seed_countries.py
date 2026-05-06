from app.utils.database import SessionLocal
from app.models.google_trends import Country

db = SessionLocal()

countries = [
    ("MW", "MWI", "Malawi"),
    ("US", "USA", "United States"),
    ("IN", "IND", "India"),
    ("ZA", "ZAF", "South Africa"),
    ("GB", "GBR", "United Kingdom"),
    ("CA", "CAN", "Canada"),
    ("AU", "AUS", "Australia"),
]

for iso2, iso3, name in countries:

    exists = (
        db.query(Country)
        .filter(Country.iso2 == iso2)
        .first()
    )

    if not exists:

        db.add(
            Country(
                iso2=iso2,
                iso3=iso3,
                name=name,
            )
        )

        print(f"✅ Added {name}")

db.commit()
db.close()

print("🌍 Countries seeded successfully")