from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import CategoryService


router = APIRouter(
    tags=["Categories"],
)


@router.post(
    "/restaurants/{restaurant_id}/categories",
    response_model=CategoryResponse,
)
def create_category(
    restaurant_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.create(
        restaurant_id,
        category_data,
    )


@router.get(
    "/restaurants/{restaurant_id}/categories",
    response_model=list[CategoryResponse],
)
def get_categories(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.get_all_by_restaurant(
        restaurant_id,
    )


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    category = service.get_by_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    category = service.update(
        category_id,
        category_data,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.delete(
    "/categories/{category_id}",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    deleted = service.delete(category_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return {
        "message": "Category deleted successfully",
    }