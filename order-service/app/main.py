from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import Base, engine
from app.routers import order_router
from app.services.kafka_producer import kafka_producer
from app.config import settings
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

async def create_kafka_topics():
    try:
        admin = AIOKafkaAdminClient(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )
        await admin.start()
        topics = [
            NewTopic(name="order-created", num_partitions=1, replication_factor=1),
            NewTopic(name="payment-confirmed", num_partitions=1, replication_factor=1),
            NewTopic(name="payment-failed", num_partitions=1, replication_factor=1),
            NewTopic(name="download-unlocked", num_partitions=1, replication_factor=1),
            NewTopic(name="product-created", num_partitions=1, replication_factor=1),
        ]
        await admin.create_topics(topics)
        print("Kafka topics created successfully!")
    except Exception as e:
        print(f"Kafka topics already exist or error: {e}")
    finally:
        await admin.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_kafka_topics()
    await kafka_producer.start()
    yield
    await kafka_producer.stop()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(order_router.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}