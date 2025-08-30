from sqlalchemy import Column, String, ARRAY
from .base_model import Base


class ContentSummary(Base):
    __tablename__ = "content_summaries"

    topic_id = Column(String(length=12), index=True, foreign_key="topics.id")
    user_id = Column(String(length=12), index=True, foreign_key="users.id")
    content_id = Column(
        String(length=12),
        index=True,
        foreign_key="content.id"
    )
    summary = Column(String)
