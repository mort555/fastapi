from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order import OrderService
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)


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

    try:
        order = service.create(order_data)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return order


@router.get(
    "",
    response_model=list[OrderResponse],
)
def get_orders(
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    return service.get_all()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    order = service.get_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order
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

    try:
        return service.change_status(
            order_id,
            status_data.status,
        )
    except ValueError as error:
        message = str(error)

        if message == "Order not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )
    