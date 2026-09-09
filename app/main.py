from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Category, Product
from app.routers.restaurants import router as restaurants_router
from app.schemas.category import CategoryCreate
from app.schemas.product import ProductCreate


app = FastAPI(title="FoodHub API")


app.include_router(restaurants_router)


@app.get("/")
async def root():
    return {"message": "FoodHub API"}


# =========================
# Categories
# =========================

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()

    return categories


@app.post("/categories")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    new_category = Category(
        name=category.name,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@app.get("/categories/{category_id}")
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully",
    }


# =========================
# Products
# =========================

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return products


@app.post("/products")
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    new_product = Product(
        name=product_data.name,
        sku=product_data.sku,
        price=product_data.price,
        cost_price=product_data.cost_price,
        supplier_id=product_data.supplier_id,
        stock=product_data.stock,
        category_id=product_data.category_id,
        unit_id=product_data.unit_id,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    product.name = product_data.name
    product.sku = product_data.sku
    product.price = product_data.price
    product.cost_price = product_data.cost_price
    product.supplier_id = product_data.supplier_id
    product.stock = product_data.stock
    product.category_id = product_data.category_id
    product.unit_id = product_data.unit_id

    db.commit()
    db.refresh(product)

    return product


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully",
    }