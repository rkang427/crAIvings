from sqlalchemy import func
from sqlalchemy.orm import Session

from ..model.restaurant import Restaurant


class RestaurantService:
    def search_restaurant(self, db: Session, input: str) -> list:
        results = db.query(Restaurant).filter(Restaurant.search_vector.op('@@')
                                              (func.plainto_tsquery(input))).all()
        return results