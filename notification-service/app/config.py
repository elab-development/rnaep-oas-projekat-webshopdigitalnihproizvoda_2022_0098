from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://notification-db:27017/notification_db"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()