import json
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from app.config import settings

TOPICS = [
    "order-created",
    "payment-confirmed",
    "payment-failed",
    "download-unlocked",
    "product-created"
]

class KafkaProducerService:
    def __init__(self):
        self.producer = None

    async def create_topics(self):
        try:
            admin = AIOKafkaAdminClient(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
            )
            await admin.start()
            topics = [
                NewTopic(name=t, num_partitions=1, replication_factor=1)
                for t in TOPICS
            ]
            await admin.create_topics(topics)
            print("Kafka topics created successfully!")
            await admin.close()
        except Exception as e:
            print(f"Kafka topics already exist or error: {e}")

    async def start(self):
        retries = 0
        max_retries = 10
        while retries < max_retries:
            try:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
                await self.producer.start()
                await self.create_topics()
                print("Kafka producer started successfully")
                return
            except Exception as e:
                retries += 1
                print(f"Kafka connection attempt {retries}/{max_retries} failed: {e}")
                await asyncio.sleep(5)
        print("Could not connect to Kafka after max retries")

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_event(self, topic: str, event: dict):
        if self.producer:
            try:
                await self.producer.send_and_wait(topic, event)
            except Exception as e:
                print(f"Failed to send Kafka event: {e}")

kafka_producer = KafkaProducerService()