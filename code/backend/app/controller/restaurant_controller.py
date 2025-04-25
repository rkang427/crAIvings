from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
import logging

from ..service.restaurant_service import RestaurantService
from ..presenter.restaurant_presenter import RestaurantPresenter
from ..db.repository import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get("/search", response_model=List[Dict])
def search_restaurants(query: str, db: Session = Depends(get_db)):
    restaurant_service = RestaurantService()
    presenter = RestaurantPresenter()

    results = restaurant_service.search_restaurant(db, query)
    formatted_results = presenter.present_search_results(results)
    #print("yay")
    return formatted_results

