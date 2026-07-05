from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import Base, engine
from app.routers import product_router, category_router
from app.services.kafka_producer import kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.start()
    yield
    await kafka_producer.stop()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(product_router.router)
app.include_router(category_router.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "product-service"}