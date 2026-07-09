from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate
from typing import Optional
import uuid

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: uuid.UUID):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all(self, search: Optional[str] = None, category_id: Optional[uuid.UUID] = None,
                min_price: Optional[float] = None, max_price: Optional[float] = None):
        query = self.db.query(Product).filter(Product.is_active == True)

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        return query.all()

    def get_by_seller(self, seller_id: uuid.UUID):
        return self.db.query(Product).filter(Product.seller_id == seller_id).all()

    def create(self, product_data: ProductCreate, seller_id: uuid.UUID, thumbnail_url: str):
        product = Product(
            seller_id=seller_id,
            category_id=product_data.category_id,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            file_path=product_data.file_path,
            thumbnail_url=thumbnail_url
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: dict):
        for key, value in data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        product.is_active = False
        self.db.commit()
        return product