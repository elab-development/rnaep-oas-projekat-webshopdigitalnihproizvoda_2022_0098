import json
import asyncio
from aiokafka import AIOKafkaConsumer
from app.config import settings

async def process_order_event(data: dict):
    """
    Poslovna logika koja se izvršava kada se konzumira order-created događaj.
    Procesira plaćanje i objavljuje payment-confirmed ili payment-failed.
    """
    from app.services.kafka_producer import kafka_producer
    from app.services.mock_payment_service import process_payment
    from app.database import SessionLocal
    from app.repositories.order_repository import OrderRepository
    from app.models.order import OrderStatus
    import secrets
    from datetime import datetime, timedelta

    db = SessionLocal()
    try:
        repo = OrderRepository(db)
        order = repo.get_by_id(data["order_id"])

        if not order:
            print(f"Order {data['order_id']} not found")
            return

        # Ažurira status na payment_processing
        repo.update_status(order, OrderStatus.payment_processing)

        # Procesira plaćanje — POSLOVNA LOGIKA
        payment_result = process_payment(float(order.amount))

        if payment_result["status"] == "success":
            # Ažurira status na confirmed
            order = repo.update_status(
                order,
                OrderStatus.confirmed,
                payment_result["transaction_id"]
            )

            # Generiše download token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            order = repo.set_download_token(order, token, expires_at)

            # Objavljuje payment-confirmed na novi topic
            await kafka_producer.send_event("payment-confirmed", {
                "order_id": str(order.id),
                "buyer_id": str(order.buyer_id),
                "seller_id": str(order.seller_id),
                "product_id": str(order.product_id),
                "amount": float(order.amount)
            })

            # Objavljuje download-unlocked
            await kafka_producer.send_event("download-unlocked", {
                "order_id": str(order.id),
                "buyer_id": str(order.buyer_id),
                "product_id": str(order.product_id)
            })

            print(f"Order {order.id} confirmed and download unlocked")

        else:
            # Ažurira status na failed
            repo.update_status(order, OrderStatus.failed)

            # Objavljuje payment-failed na novi topic
            await kafka_producer.send_event("payment-failed", {
                "order_id": str(order.id),
                "buyer_id": str(order.buyer_id),
                "reason": payment_result["reason"]
            })

            print(f"Order {order.id} payment failed")

    finally:
        db.close()


async def start_order_kafka_consumer():
    """
    Kafka Consumer koji konzumira order-created događaje,
    izvršava poslovnu logiku plaćanja i objavljuje nove događaje.
    Ovo čini Order Service hibridnim modulom — i Consumer i Producer.
    """
    retries = 0
    max_retries = 10
    consumer = None

    while retries < max_retries:
        try:
            consumer = AIOKafkaConsumer(
                "order-created",
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id="order-service-group",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest"
            )
            await consumer.start()
            print("Order Service Kafka Consumer started!")
            break
        except Exception as e:
            retries += 1
            print(f"Order consumer attempt {retries}/{max_retries} failed: {e}")
            await asyncio.sleep(5)

    if consumer is None:
        print("Could not start Order Service Kafka Consumer")
        return

    try:
        async for message in consumer:
            print(f"Order Service consumed: {message.topic} - {message.value}")
            await process_order_event(message.value)
    finally:
        await consumer.stop()