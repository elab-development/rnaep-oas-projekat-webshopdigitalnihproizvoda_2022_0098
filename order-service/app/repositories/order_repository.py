from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderStatus
import uuid

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: uuid.UUID):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_by_buyer(self, buyer_id: uuid.UUID):
        return self.db.query(Order).filter(Order.buyer_id == buyer_id).all()

    def has_purchased(self, buyer_id: uuid.UUID, product_id: uuid.UUID):
        return self.db.query(Order).filter(
            Order.buyer_id == buyer_id,
            Order.product_id == product_id,
            Order.status == OrderStatus.confirmed
        ).first() is not None

    def create(self, buyer_id: uuid.UUID, product_id: uuid.UUID, seller_id: uuid.UUID, amount: float):
        order = Order(
            buyer_id=buyer_id,
            product_id=product_id,
            seller_id=seller_id,
            amount=amount,
            status=OrderStatus.pending
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order: Order, status: OrderStatus, payment_reference: str = None):
        order.status = status
        if payment_reference:
            order.payment_reference = payment_reference
        self.db.commit()
        self.db.refresh(order)
        return order

    def set_download_token(self, order: Order, token: str, expires_at):
        order.download_token = token
        order.token_expires_at = expires_at
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_sales_stats_by_seller(self, seller_id: uuid.UUID):
        results = self.db.query(
            Order.product_id,
            func.count(Order.id).label("total_sales"),
            func.sum(Order.amount).label("total_revenue")
        ).filter(
            Order.seller_id == seller_id,
            Order.status == OrderStatus.confirmed
        ).group_by(Order.product_id).all()
        return results