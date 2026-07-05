from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import Base, engine
from app.routers import auth_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}