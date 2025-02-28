from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    jwt_audience: str = os.getenv("JWT_AUDIENCE")
    jwt_issuer: str = os.getenv("JWT_ISSUER")
    jwks_url: str = os.getenv("JWKS_URL")


settings = Settings()
