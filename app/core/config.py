
import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Property Manager"
    API_V1_STR: str = "/api/v1"
    pg_host = os.getenv("PG_HOST")
    pg_password = os.getenv("PG_PASSWORD")
    pg_user = os.getenv("PG_USER")
    pg_db = os.getenv("PG_DB")
    pg_port = os.getenv("PG_PORT")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

settings = Settings()
