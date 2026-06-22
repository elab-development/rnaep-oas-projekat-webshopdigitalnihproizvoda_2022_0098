from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta
import secrets
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, SalesStatsResponse, PricesInCurrencies
from app.repositories.order_repository import OrderRepository
from app.clients.product_client import get_product_details
from app.clients.exchange_rate_client import get_prices_in_currencies
from app.services.mock_payment_service import process_payment
from app.services.kafka_producer import kafka_producer
from app.services.auth_dependency import get_current_user
from app.models.order import OrderStatus
from decimal import Decimal

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order_data: OrderCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = OrderRepository(db)

    # 1. Proveri da kupac već ne poseduje proizvod (FK-16)
    if repo.has_purchased(current_user["user_id"], order_data.product_id):
        raise HTTPException(status_code=400, detail="You already own this product")

    # 2. Pribavi podatke o proizvodu sa Product Service-a
    product = await get_product_details(str(order_data.product_id), current_user["token"])
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 3. Kreiraj narudžbinu u statusu pending
    order = repo.create(
        buyer_id=current_user["user_id"],
        product_id=order_data.product_id,
        seller_id=product["seller_id"],
        amount=product["price"]
    )

    # 4. Objavi order-created događaj
    await kafka_producer.send_event("order-created", {
        "order_id": str(order.id),
        "buyer_id": str(order.buyer_id),
        "product_id": str(order.product_id),
        "amount": float(order.amount)
    })

    # 5. Procesiraj plaćanje (mock)
    repo.update_status(order, OrderStatus.payment_processing)
    payment_result = process_payment(float(order.amount))

    if payment_result["status"] == "success":
        # 6a. Plaćanje uspešno → potvrdi narudžbinu
        order = repo.update_status(order, OrderStatus.confirmed, payment_result["transaction_id"])

        await kafka_producer.send_event("payment-confirmed", {
            "order_id": str(order.id),
            "buyer_id": str(order.buyer_id),
            "seller_id": str(order.seller_id),
            "product_id": str(order.product_id),
            "amount": float(order.amount)
        })

        # 7. Generiši download token (FK-15)
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        order = repo.set_download_token(order, token, expires_at)

        await kafka_producer.send_event("download-unlocked", {
            "order_id": str(order.id),
            "buyer_id": str(order.buyer_id),
            "product_id": str(order.product_id)
        })
    else:
        # 6b. Plaćanje neuspešno → kompenzaciona akcija (rollback statusa)
        order = repo.update_status(order, OrderStatus.failed)
        await kafka_producer.send_event("payment-failed", {
            "order_id": str(order.id),
            "buyer_id": str(order.buyer_id),
            "reason": payment_result["reason"]
        })
        raise HTTPException(status_code=402, detail="Payment failed")

    return order

@router.get("/my-purchases", response_model=list[OrderResponse])
def get_my_purchases(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    return repo.get_by_buyer(current_user["user_id"])

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # IDOR zaštita — samo kupac ili admin može videti narudžbinu
    if str(order.buyer_id) != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have access to this order")
    return order

@router.get("/{order_id}/download")
def download_product(order_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if str(order.buyer_id) != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    if order.status != OrderStatus.confirmed:
        raise HTTPException(status_code=400, detail="Order not confirmed")
    if order.token_expires_at and order.token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Download link expired")
    return {"download_token": order.download_token, "product_id": str(order.product_id)}

@router.get("/seller/stats", response_model=list[SalesStatsResponse])
def get_sales_stats(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view sales stats")
    repo = OrderRepository(db)
    results = repo.get_sales_stats_by_seller(current_user["user_id"])
    return [
        SalesStatsResponse(product_id=r.product_id, total_sales=r.total_sales, total_revenue=r.total_revenue)
        for r in results
    ]

@router.get("/exchange/{amount}", response_model=PricesInCurrencies)
async def get_price_in_currencies(amount: Decimal):
    prices = await get_prices_in_currencies(amount)
    return prices