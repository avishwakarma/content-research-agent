from sqlalchemy import Column, String
from .base_model import Base


class UserTopic(Base):
    __tablename__ = "user_topics"

    user_id = Column(String(length=12), index=True, foreign_key="users.id")
    topic_id = Column(String(length=12), index=True, foreign_key="topics.id")
