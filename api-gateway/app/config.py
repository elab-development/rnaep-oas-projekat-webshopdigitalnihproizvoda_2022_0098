from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user-service:8000"
    PRODUCT_SERVICE_URL: str = "http://product-service:8000"
    ORDER_SERVICE_URL: str = "http://order-service:8000"
    NOTIFICATION_SERVICE_URL: str = "http://notification-service:8000"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()