from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppException
from app.routers import (
    categories,
    customers,
    dishes,
    orders,
    restaurants,
    reviews,
)


app = FastAPI(
    title="FoodHub API",
    version="0.1.0",
)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(restaurants.router)
app.include_router(categories.router)
app.include_router(dishes.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(reviews.router)


@app.get("/")
def root():
    return {"message": "FoodHub API"}