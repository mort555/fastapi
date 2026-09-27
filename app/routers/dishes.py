from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.dish import (
    DishCreate,
    DishListResponse,
    DishResponse,
    DishUpdate,
)
from app.services.dish import DishService


router = APIRouter(
    prefix="",
    tags=["Dishes"],
)


@router.post(
    "/restaurants/{restaurant_id}/dishes",
    response_model=DishResponse,
)
def create_dish(
    restaurant_id: int,
    dish_data: DishCreate,
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.create(
        restaurant_id,
        dish_data,
    )


@router.get(
    "/restaurants/{restaurant_id}/dishes",
    response_model=DishListResponse,
)
def get_dishes(
    restaurant_id: int,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    is_available: bool | None = None,
    search: str | None = None,
    ordering: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.get_all_by_restaurant(
        restaurant_id=restaurant_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available,
        search=search,
        ordering=ordering,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/dishes/{dish_id}",
    response_model=DishResponse,
)
def get_dish(
    dish_id: int,
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.get_by_id(
        dish_id,
    )


@router.patch(
    "/dishes/{dish_id}",
    response_model=DishResponse,
)
def update_dish(
    dish_id: int,
    dish_data: DishUpdate,
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.update(
        dish_id,
        dish_data,
    )


@router.delete(
    "/dishes/{dish_id}",
)
def delete_dish(
    dish_id: int,
    db: Session = Depends(get_db),
):
    service = DishService(db)

    service.delete(
        dish_id,
    )

    return {
        "message": "Dish deleted successfully",
    }