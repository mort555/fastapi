from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant import RestaurantService


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post(
    "",
    response_model=RestaurantResponse,
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.create(restaurant_data)


@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_all()


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    restaurant = service.get_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return restaurant


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    restaurant = service.update(
        restaurant_id,
        restaurant_data,
    )

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return restaurant


@router.delete(
    "/{restaurant_id}",
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    deleted = service.delete(restaurant_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return {
        "message": "Restaurant deleted successfully",
    }