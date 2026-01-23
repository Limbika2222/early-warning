from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.utils.database import engine
from app.models.google_trends import GoogleTrendsTimeseries

Session = sessionmaker(bind=engine)

def store_trends(keyword_id: int, country_id: int, df):
    db = Session()

    for _, row in df.iterrows():
        record = GoogleTrendsTimeseries(
            keyword_id=keyword_id,
            country_id=country_id,
            date=row["date"],
            interest_index=int(row["interest_index"]),
            fetched_at=datetime.utcnow(),
        )
        db.add(record)

    db.commit()
