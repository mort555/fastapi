from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
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

    dish = service.create(
        restaurant_id,
        dish_data,
    )

    if dish is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found in this restaurant",
        )

    return dish


@router.get(
    "/restaurants/{restaurant_id}/dishes",
    response_model=DishListResponse,
)
def get_dishes(
    restaurant_id: int,
    category_id: int | None = Query(None),
    min_price: Decimal | None = Query(None),
    max_price: Decimal | None = Query(None),
    is_available: bool | None = Query(None),
    search: str | None = Query(None),
    ordering: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.get_filtered_by_restaurant(
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

    dish = service.get_by_id(dish_id)

    if dish is None:
        raise HTTPException(
            status_code=404,
            detail="Dish not found",
        )

    return dish


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

    dish = service.update(
        dish_id,
        dish_data,
    )

    if dish is None:
        raise HTTPException(
            status_code=404,
            detail="Dish not found",
        )

    return dish


@router.delete(
    "/dishes/{dish_id}",
)
def delete_dish(
    dish_id: int,
    db: Session = Depends(get_db),
):
    service = DishService(db)

    deleted = service.delete(dish_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dish not found",
        )

    return {
        "message": "Dish deleted successfully",
    }