from sqlalchemy import Column, String
from .base_model import Base


class Topic(Base):
    __tablename__ = "topics"

    title = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
