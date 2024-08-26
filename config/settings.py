from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./blog-site.db"


settings = Settings()
