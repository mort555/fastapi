from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.filtering import OrderFilterParams
from app.dependencies import get_db
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)
from app.services.order import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderResponse,
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    return service.create(order_data)


@router.get(
    "",
)
def get_orders(
    params: OrderFilterParams = Depends(),
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    return service.get_filtered(params)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    return service.get_by_id(order_id)


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def change_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    return service.change_status(
        order_id,
        status_data.status,
    )