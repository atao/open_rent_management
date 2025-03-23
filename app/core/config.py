import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Property Manager"
    API_V1_STR: str = "/api/v1"
    pg_host = os.getenv("PG_HOST", "localhost")
    pg_password = os.getenv("PG_PASSWORD", "password")
    pg_user = os.getenv("PG_USER", "user")
    pg_db = os.getenv("PG_DB", "database")
    pg_port = os.getenv("PG_PORT", "5432")
    secret_key = os.getenv("SECRET_KEY", "your-secret-key")
    algorithm = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


settings = Settings()
