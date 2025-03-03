from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    SENDGRID_API_KEY: str
    FROM_EMAIL: str
    ENVIRONMENT: str
    PORT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
