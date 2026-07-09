from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import user_routes, product_routes, order_routes, notification_routes
from app.circuit_breaker import circuit_breakers

app = FastAPI(title="API Gateway")

# CORS konfiguracija — dozvoljen samo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)
app.include_router(notification_routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/circuit-breakers/status")
def get_circuit_breaker_status():
    """Endpoint za pregled statusa svih Circuit Breaker-a."""
    return {
        service: cb.get_status()
        for service, cb in circuit_breakers.items()
    }