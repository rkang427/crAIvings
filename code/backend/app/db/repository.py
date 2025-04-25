from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from code.backend.app.model.restaurant import Restaurant
from code.backend.app.model.restaurant_parking import Parking

engine = create_engine('postgresql://craivings_user:password@localhost/db_craivings')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_restaurant(db: Session):
    return db.query(Restaurant).all()

def fetch_parking(db: Session):
    return db.query(Parking).all()