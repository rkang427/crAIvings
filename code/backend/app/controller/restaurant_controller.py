from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from transformers import pipeline

from ..service.restaurant_service import RestaurantService
from ..presenter.restaurant_presenter import RestaurantPresenter
from ..db.repository import get_db

router = APIRouter()

@router.get("/restaurant/recommendations", response_model=List[Dict])
def search_restaurants(query: str, db: Session = Depends(get_db)):
    restaurant_service = RestaurantService()
    restaurant_presenter = RestaurantPresenter()

    results = restaurant_service.search_restaurant(db, query)
    formatted_results = restaurant_presenter.present_search_results(results)
    return formatted_results
#
# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')
#
# @router.post("/predict/")
# async def predict(payload: dict):
#     text = payload.get("text", "")
#     result = generator(text)
#     return {"yes": result}