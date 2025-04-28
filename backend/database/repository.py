from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..model.restaurant import Restaurant
from ..model.restaurant_parking import Parking
from ..model.restaurant_category import RestaurantCategory
from ..model.restaurant_hours import Hours

engine = create_engine('postgresql://craivings_user:password@localhost/db_craivings')
engine_neon = create_engine(
    "postgresql://neondb_owner:npg_2Ul5ykzTcRNX@ep-round-wave-a4ppyklf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&options=endpoint%3Dep-round-wave-a4ppyklf"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_neon)

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

def fetch_categories(db: Session):
    return db.query(RestaurantCategory).all()

def fetch_s(db: Session):
    return db.query(RestaurantCategory).all()

def fetch_hours(db: Session):
    return db.query(Hours).all()