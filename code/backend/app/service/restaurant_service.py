from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from ..model.restaurant import Restaurant

engine = create_engine('postgresql://craivings_user:password@localhost/db_craivings')
Session = sessionmaker(
    bind=engine)  # sessionmaker is a factory that binds the engine (which connects to the database) and creates a Session class.
# defining how to interact with your database using this Session class.
class RestaurantService:
    def __init__(self, session:Session):
        self.session = session
    def search_restaurant(self, input: str) -> list: #means that it returns nothing like void
        with self.session as session:
            results = session.query(Restaurant).filter(Restaurant.search_vector.op('@@')(func.plainto_tsquery(input))).all()
            return [f"{restaurant.name} at {restaurant.city}, {restaurant.state}" for restaurant in results]

def __main__():
    print("Hello there! What would you like to eat?")
    user_input = input()
    with Session() as session:
        restaurant_service = RestaurantService(session)
        results = restaurant_service.search_restaurant(user_input)
        if results:
            print("\n".join(results))

if __name__ == "__main__":
    __main__()
