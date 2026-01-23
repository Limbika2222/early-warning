from sqlalchemy.orm import sessionmaker

from app.utils.database import engine
from app.models.google_trends import Disease, Country

Session = sessionmaker(bind=engine)
db = Session()

def seed_diseases():
    diseases = [
        Disease(name="Influenza", code="ILI"),
        Disease(name="Malaria", code="MAL"),
        Disease(name="Cholera", code="CHOL"),
        Disease(name="Zika", code="ZIKA"),
    ]
    db.add_all(diseases)
    db.commit()

def seed_countries():
    countries = [
        Country(name="India", iso2="IN", iso3="IND"),
        Country(name="United States", iso2="US", iso3="USA"),
        Country(name="Brazil", iso2="BR", iso3="BRA"),
        Country(name="Malawi", iso2="MW", iso3="MWI"),
        Country(name="Philippines", iso2="PH", iso3="PHL"),
        
    ]
    db.add_all(countries)
    db.commit()

if __name__ == "__main__":
    seed_diseases()
    seed_countries()
    print("✅ Diseases and countries seeded successfully")
