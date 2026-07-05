from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    EXCHANGE_RATE_API_URL: str = "https://api.frankfurter.app"

    class Config:
        env_file = ".env"

settings = Settings()