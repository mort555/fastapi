from fastapi import FastAPI

from app.routers.categories import router as categories_router
from app.routers.customers import router as customers_router
from app.routers.dishes import router as dishes_router
from app.routers.orders import router as orders_router
from app.routers.restaurants import router as restaurants_router
from app.routers.reviews import router as reviews_router

app = FastAPI(
    title="FoodHub API",
)

app.include_router(reviews_router)
app.include_router(restaurants_router)
app.include_router(categories_router)
app.include_router(dishes_router)
app.include_router(customers_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {
        "message": "FoodHub API",
    }