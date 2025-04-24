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

    def __init__(self, id, name, address, city, state, postal_code,
                 latitude, longitude, stars, review_count, is_open, search_vector=None):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.stars = stars
        self.review_count = review_count
        self.is_open = is_open
        self.search_vector = search_vector
