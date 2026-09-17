from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def get_all(self) -> list[Customer]:
        return self.repository.get_all()

    def get_by_id(
        self,
        customer_id: int,
    ) -> Customer | None:
        return self.repository.get_by_id(customer_id)

    def create(
        self,
        customer_data: CustomerCreate,
    ) -> Customer | None:

        existing_customer = self.repository.get_by_email(
            str(customer_data.email),
        )

        if existing_customer is not None:
            return None

        customer = Customer(
            name=customer_data.name,
            email=str(customer_data.email),
            phone=customer_data.phone,
        )

        return self.repository.create(customer)

    def update(
        self,
        customer_id: int,
        customer_data: CustomerUpdate,
    ) -> Customer | None:

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            return None

        update_data = customer_data.model_dump(
            exclude_unset=True,
        )

        if "email" in update_data:
            existing_customer = self.repository.get_by_email(
                update_data["email"],
            )

            if (
                existing_customer is not None
                and existing_customer.id != customer_id
            ):
                return None

        for field, value in update_data.items():
            setattr(customer, field, value)

        return self.repository.update(customer)

    def delete(
        self,
        customer_id: int,
    ) -> bool:

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            return False

        self.repository.delete(customer)

        return True