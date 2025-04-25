from fastapi import FastAPI, Query, Depends
from code.backend.app.controller.restaurant_controller import router as restaurant_router

app = FastAPI()
app.include_router(restaurant_router)