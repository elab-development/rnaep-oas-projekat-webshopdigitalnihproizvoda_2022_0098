from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    UNSPLASH_ACCESS_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"

    class Config:
        env_file = ".env"

settings = Settings()