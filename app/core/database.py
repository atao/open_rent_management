from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings

database_url = (
    f"postgresql://{Settings.pg_user}:{Settings.pg_password}@{Settings.pg_host}:{Settings.pg_port}/{Settings.pg_db}"
)

SQLALCHEMY_DATABASE_URL = database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
