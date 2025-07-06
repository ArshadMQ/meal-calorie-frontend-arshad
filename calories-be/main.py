"""
Main module for the client admin FastAPI application.

This (main.py) module sets up the FastAPI application, including configuration,
middleware, and route inclusion. It is the entry point for the client admin
API, handling CORS settings and serving the API documentation.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database.connection import Base, engine
from utils.ratelimiter import RateLimitMiddleware
# ----------------Importing Routes Start--------------------------

from routers import (
    sign_in_up_router,
    calories_router,
)

# ----------------Routes end------------------------------

app = FastAPI(
    title="Calories application backend service",
    openapi_url="/swagger/_openapi.json",
    docs_url="/swagger/_docs",
    redoc_url="/swagger/_redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://mealory.arshadmq.com",
                   "http://mealory.arshadmq.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)


@app.get("/")
async def index():
    """
    Root endpoint for the calories application backend service

    Return the status code and welcome message
    """
    return {"status": 200, "detail": "Welcome to calories application backend service"}


app.include_router(sign_in_up_router)
app.include_router(calories_router)

# Create all database tables
Base.metadata.create_all(bind=engine)
