from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.filtering import DishFilterParams
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
    params: DishFilterParams = Depends(),
    db: Session = Depends(get_db),
):
    service = DishService(db)

    return service.get_all_by_restaurant(
        restaurant_id=restaurant_id,
        category_id=params.category_id,
        min_price=params.min_price,
        max_price=params.max_price,
        is_available=params.is_available,
        search=params.search,
        ordering=params.ordering,
        page=params.page,
        page_size=params.page_size,
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