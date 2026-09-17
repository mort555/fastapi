from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

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
    response_model=RestaurantListResponse,
)
def get_restaurants(
    search: str | None = None,
    is_active: bool | None = None,
    min_rating: float | None = Query(
        default=None,
        ge=0,
        le=5,
    ),
    ordering: str | None = None,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_filtered(
        search=search,
        is_active=is_active,
        min_rating=min_rating,
        ordering=ordering,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{restaurant_id}/statistics",
    response_model=RestaurantStatisticsResponse,
)
def get_restaurant_statistics(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    statistics = service.get_statistics(
        restaurant_id,
    )

    if statistics is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return statistics


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

    try:
        sales = service.get_sales(
            restaurant_id,
            date_from,
            date_to,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if sales is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return sales


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    restaurant = service.get_by_id(
        restaurant_id,
    )

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

    deleted = service.delete(
        restaurant_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return {
        "message": "Restaurant deleted successfully",
    }