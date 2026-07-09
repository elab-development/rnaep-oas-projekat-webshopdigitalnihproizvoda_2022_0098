from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import Base, engine
from app.routers import order_router
from app.services.kafka_producer import kafka_producer
from app.services.kafka_consumer import start_order_kafka_consumer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.start()
    # Pokreće Kafka Consumer kao background task
    consumer_task = asyncio.create_task(start_order_kafka_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
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
#ovo je main file
Instrumentator().instrument(app).expose(app)

app.include_router(order_router.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}