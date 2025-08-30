from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import Base


class Content(Base):
    __tablename__ = "content"

    topic_id = Column(String(length=12), index=True, foreign_key="topics.id")
    title = Column(String)
    url = Column(String, nullable=True)
    favicon_url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    image_alt = Column(String, nullable=True)
    raw_content = Column(String, nullable=True)
    tags = Column(String, nullable=True)
