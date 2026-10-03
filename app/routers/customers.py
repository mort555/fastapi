from fastapi import APIRouter, Depends
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

    return service.create(customer_data)


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

    return service.get_by_id(customer_id)


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

    return service.update(
        customer_id,
        customer_data,
    )


@router.delete(
    "/{customer_id}",
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    service.delete(customer_id)

    return {
        "message": "Customer deleted successfully",
    }