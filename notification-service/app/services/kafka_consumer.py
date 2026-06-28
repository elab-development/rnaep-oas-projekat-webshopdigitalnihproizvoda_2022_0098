import json
import asyncio
from aiokafka import AIOKafkaConsumer
from app.config import settings
from app.database import get_collection
from app.models.notification import Notification, NotificationType
from app.repositories.notification_repository import NotificationRepository

TOPICS = [
    "product-created",
    "order-created",
    "payment-confirmed",
    "payment-failed",
    "download-unlocked"
]

async def handle_event(topic: str, data: dict):
    """Kreira notifikaciju na osnovu tipa Kafka događaja."""
    collection = get_collection()
    repo = NotificationRepository(collection)

    if topic == "payment-confirmed":
        # Notifikacija za kupca
        await repo.create(Notification(
            user_id=data["buyer_id"],
            type=NotificationType.order_confirmed,
            title="Kupovina uspešna",
            message=f"Uspešno ste kupili proizvod. Iznos: {data['amount']} RSD",
            metadata={"order_id": data["order_id"], "product_id": data["product_id"]}
        ))
        # Notifikacija za prodavca
        await repo.create(Notification(
            user_id=data["seller_id"],
            type=NotificationType.new_sale,
            title="Nova prodaja",
            message=f"Neko je kupio vaš proizvod. Zarada: {data['amount']} RSD",
            metadata={"order_id": data["order_id"], "product_id": data["product_id"]}
        ))

    elif topic == "payment-failed":
        await repo.create(Notification(
            user_id=data["buyer_id"],
            type=NotificationType.payment_failed,
            title="Plaćanje neuspešno",
            message="Vaše plaćanje nije uspelo. Pokušajte ponovo.",
            metadata={"order_id": data["order_id"]}
        ))

    elif topic == "download-unlocked":
        await repo.create(Notification(
            user_id=data["buyer_id"],
            type=NotificationType.download_unlocked,
            title="Preuzimanje dostupno",
            message="Vaš proizvod je spreman za preuzimanje.",
            metadata={"order_id": data["order_id"], "product_id": data["product_id"]}
        ))

    elif topic == "product-created":
        await repo.create(Notification(
            user_id=data["seller_id"],
            type=NotificationType.product_created,
            title="Proizvod objavljen",
            message=f"Vaš proizvod '{data['name']}' je uspešno objavljen na platformi.",
            metadata={"product_id": data["product_id"]}
        ))

async def start_kafka_consumer():
    """Pokreće Kafka consumer koji sluša sve relevantne topice."""
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="notification-service-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest"
    )

    await consumer.start()
    try:
        async for message in consumer:
            await handle_event(message.topic, message.value)
    finally:
        await consumer.stop()