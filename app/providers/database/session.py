# Why: engine and database session lifecycle live outside business services.
import os
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

@lru_cache(maxsize=1)
def get_engine():
    url = os.getenv("DATABASE_URL","postgresql+psycopg://invoice:invoice@localhost:5432/invoice_db")
    return create_engine(url, pool_pre_ping=True)

@lru_cache(maxsize=1)
def get_session_factory():
    return sessionmaker(bind=get_engine(), class_=Session, expire_on_commit=False)

def get_db_session() -> Session:
    return get_session_factory()()
