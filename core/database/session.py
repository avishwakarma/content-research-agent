from functools import lru_cache
from sqlalchemy.orm import sessionmaker, Session
from core.models.base_model import Base
from .sqlite_engine import engine

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@lru_cache
def get_session() -> Session:
    return SessionLocal()


session = get_session()
