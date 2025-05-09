from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.controller.restaurant_controller import router
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://craivings.vercel.app",
    "localhost/:1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)
