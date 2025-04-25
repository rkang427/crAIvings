from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'  # psql table name

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    stars = Column(Float, nullable=False)
    review_count = Column(Integer, nullable=False)
    is_open = Column(Boolean, nullable=False)
    search_vector = Column(TSVECTOR)
