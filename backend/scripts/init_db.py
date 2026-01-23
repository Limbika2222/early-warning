from app.utils.database import engine
from app.models.google_trends import Base

Base.metadata.create_all(bind=engine)
