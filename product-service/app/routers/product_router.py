from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.repositories.product_repository import ProductRepository
from app.clients.unsplash_client import get_product_thumbnail
from app.services.kafka_producer import kafka_producer
from app.services.auth_dependency import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_products(
    search: Optional[str] = None,
    category_id: Optional[UUID] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    return repo.get_all(search, category_id, min_price, max_price)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/seller/my-products", response_model=list[ProductResponse])
def get_my_products(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_by_seller(current_user["user_id"])

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product_data: ProductCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can create products")

    thumbnail_url = await get_product_thumbnail(product_data.name)

    repo = ProductRepository(db)
    product = repo.create(product_data, current_user["user_id"], thumbnail_url)

    await kafka_producer.send_event("product-created", {
        "product_id": str(product.id),
        "seller_id": str(product.seller_id),
        "name": product.name,
        "price": float(product.price)
    })

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, update_data: ProductUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # IDOR zaštita — proverava da li je korisnik vlasnik proizvoda
    if str(product.seller_id) != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to modify this product")

    data = {k: v for k, v in update_data.model_dump().items() if v is not None}
    return repo.update(product, data)

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # IDOR zaštita
    if str(product.seller_id) != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this product")

    repo.delete(product)