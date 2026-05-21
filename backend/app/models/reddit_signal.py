from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.utils.database import Base


class RedditSignal(Base):

    __tablename__ = "reddit_signals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    disease = Column(
        String,
        nullable=False,
        default="Unknown",
    )

    subreddit = Column(
        String,
        nullable=True,
    )

    title = Column(
        String,
        nullable=True,
    )

    signal_strength = Column(
        Integer,
        default=1,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )