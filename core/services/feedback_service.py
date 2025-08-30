from typing import Dict
from core.database import session
from core.models import UserFeedback, Content


class FeedbackService:
    def __init__(self):
        self.session = session

    def _feedback(self, content_id: str, user_id: str) -> UserFeedback:
        instance = self.session.query(UserFeedback).filter_by(
            content_id=content_id, user_id=user_id).first()

        if not instance:
            instance = UserFeedback(
                content_id=content_id,
                user_id=user_id
            )

        return instance

    def add_comment(self, content_id: str, user_id: str, comment: str) -> UserFeedback:
        instance = self._feedback(content_id, user_id)

        instance.comment = comment

        self.session.add(instance)
        self.session.commit()

        return instance

    def like_content(self, content_id: str, user_id: str) -> UserFeedback:
        instance = self._feedback(content_id, user_id)

        instance.liked = True

        self.session.add(instance)
        self.session.commit()
        return instance

    def read_content(self, content_id: str, user_id: str) -> UserFeedback:
        instance = self._feedback(content_id, user_id)

        instance.read = True

        self.session.add(instance)
        self.session.commit()

        return instance

    def get_feedback(self, user_id: str) -> list[Dict] | None:
        return self.session.query(
            Content,
            UserFeedback.comment.label("user_comment"),
            UserFeedback.liked.label("user_liked"),
            UserFeedback.read.label("user_read"),
        ).join(Content, UserFeedback.content_id == Content.id).filter_by(
            user_id=user_id
        ).all()
