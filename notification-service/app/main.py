from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import notification_router
from app.services.kafka_consumer import start_kafka_consumer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_kafka_consumer())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Notification Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(notification_router.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "notification-service"}