from sqlalchemy import Boolean, Column, String
from .base_model import Base


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    user_id = Column(String(length=12), index=True, foreign_key="users.id")
    topic_id = Column(String(length=12), index=True, foreign_key="topics.id")
    content_id = Column(
        String(length=12),
        index=True,
        foreign_key="content.id"
    )
    liked = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    comment = Column(String, nullable=True)
