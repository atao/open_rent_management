import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

pg_host = os.getenv("PG_HOST")
pg_password = os.getenv("PG_PASSWORD")
pg_user = os.getenv("PG_USER")
pg_db = os.getenv("PG_DB")
pg_port = os.getenv("PG_PORT")
database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

SQLALCHEMY_DATABASE_URL = database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()