from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://admin:admin@localhost:5432/main"


settings = Settings()