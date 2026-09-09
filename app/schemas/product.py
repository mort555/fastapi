from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    cost_price: float
    supplier_id: int
    stock: int
    category_id: int
    unit_id: int