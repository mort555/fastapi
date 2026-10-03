from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.filtering import RestaurantFilterParams
from app.dependencies import get_db
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantListResponse,
    RestaurantResponse,
    RestaurantSalesResponse,
    RestaurantStatisticsResponse,
    RestaurantUpdate,
)
from app.services.restaurant import RestaurantService


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.get(
    "",
    response_model=RestaurantListResponse,
)
def get_restaurants(
    params: RestaurantFilterParams = Depends(),
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_filtered(
        search=params.search,
        is_active=params.is_active,
        min_rating=params.min_rating,
        ordering=params.ordering,
        page=params.page,
        page_size=params.page_size,
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

    return service.create(
        restaurant_data,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_by_id(
        restaurant_id,
    )


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

    return service.update(
        restaurant_id,
        restaurant_data,
    )


@router.delete(
    "/{restaurant_id}",
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    service.delete(
        restaurant_id,
    )

    return {
        "message": "Restaurant deleted successfully",
    }


@router.get(
    "/{restaurant_id}/statistics",
    response_model=RestaurantStatisticsResponse,
)
def get_restaurant_statistics(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_statistics(
        restaurant_id,
    )


@router.get(
    "/{restaurant_id}/statistics/sales",
    response_model=RestaurantSalesResponse,
)
def get_restaurant_sales(
    restaurant_id: int,
    date_from: datetime,
    date_to: datetime,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_sales(
        restaurant_id,
        date_from,
        date_to,
    )