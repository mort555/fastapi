from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    customer = service.create(customer_data)

    if customer is None:
        raise HTTPException(
            status_code=409,
            detail="Customer with this email already exists",
        )

    return customer


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_customers(
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    return service.get_all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    customer = service.get_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    customer = service.update(
        customer_id,
        customer_data,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found or email already exists",
        )

    return customer


@router.delete(
    "/{customer_id}",
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    deleted = service.delete(customer_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {
        "message": "Customer deleted successfully",
    }