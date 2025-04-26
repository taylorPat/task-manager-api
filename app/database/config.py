import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


def get_database_url():
    url = os.getenv("DATABASE_URL")
    if url is None:
        raise ValueError("DATABASE_URL is None.")
    return url


engine = create_engine(get_database_url(), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
