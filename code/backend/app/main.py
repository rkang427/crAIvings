from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from code.backend.app.controller.restaurant_controller import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://craivings.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)
