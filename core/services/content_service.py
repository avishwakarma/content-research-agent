from typing import Dict
from core.database import session
from core.models import Content, ContentSummary
from core.models.topic_model import Topic
from core.models.user_feedback_model import UserFeedback
from core.tools import TavilyContent, Tavily
from core.utils import source_from_url


class ContentService:
    def __init__(self):
        self.session = session
        self.tavily = Tavily()

    def get_content_by_id(self, content_id: str) -> Content | None:
        content = self.session.query(Content).filter_by(id=content_id).first()
        return {"content_id": content.id, "raw_content": content.raw_content} if content else {}

    def get_user_summary(self, content_id: str, user_id: str) -> str | None:
        summary = self.session.query(ContentSummary).filter_by(
            content_id=content_id, user_id=user_id).first()
        return summary.summary if summary else None

    def fetch_new_content(self, topic_id: str) -> list[Dict] | None:
        topic = self.session.query(Topic).filter_by(id=topic_id).first()

        if not topic:
            return []

        content = self.tavily.find(
            topic=topic.title,
            max_results=1
        )

        if len(content) > 0:
            instances = [
                Content(
                    topic_id=topic_id,
                    title=c.title,
                    url=c.url,
                    favicon_url=c.favicon,
                    source=source_from_url(c.url),
                    image_url=c.banner,
                    image_alt=c.banner_alt,
                    raw_content=c.raw_content
                ) for c in content
            ]

            self.session.add_all(instances)
            self.session.commit()
            return instances

        return []

    def add_content(self, content: TavilyContent, topic_id: str) -> Content:
        instance = Content(
            topic_id=topic_id,
            title=content.title,
            url=content.url,
            favicon_url=content.favicon,
            source=source_from_url(content.url),
            image_url=content.banner,
            image_alt=content.banner_alt,
            raw_content=content.raw_content,
            tags=content.tags
        )
        self.session.add(instance)
        self.session.commit()
        return instance

    def add_summary(self, summary: str, content_id: str, user_id: str) -> Dict:
        print(
            f"Adding summary for content_id: {content_id} and user_id: {user_id}")
        content = self.session.query(Content).filter_by(id=content_id).first()

        if not content:
            raise ValueError("Content not found")

        hasSummary = self.session.query(ContentSummary).filter_by(
            content_id=content_id, user_id=user_id).first()

        print(
            f"Existing summary: {hasSummary.summary if hasSummary else 'None'}")

        if not hasSummary:
            hasSummary = ContentSummary(
                topic_id=content.topic_id,
                user_id=user_id,
                content_id=content_id,
                summary=summary
            )
            self.session.add(hasSummary)
            self.session.commit()
        else:
            hasSummary.summary = summary
            self.session.commit()

        content.summary = hasSummary.summary

        return {
            "content_id": content.id,
            "user_id": user_id,
            "message": "Summary updated"
        }

    def get_content_by_ids(self, content_ids: list[str], user_id: str) -> list[Dict] | None:
        print(
            f"Fetching content for user_id: {user_id} and content_ids: {content_ids}")
        content = (
            self.session.query(Content, ContentSummary.summary.label(
                'summary'), Topic.title.label('topic'))
            .join(Topic, Content.topic_id == Topic.id)
            .join(ContentSummary, (ContentSummary.content_id == Content.id) & (ContentSummary.user_id == user_id))
            .filter(Content.id.in_(content_ids))
            .filter(ContentSummary.summary.isnot(None))
            .all()
        )

        print(
            f"Fetched {len(content) if content else 0} content items for user_id: {user_id}")

        return [{
            "content_id": c.id,
            "topic_id": c.topic_id,
            "topic": topic,
            "title": c.title,
            "url": c.url,
            "favicon_url": c.favicon_url,
            "source": c.source,
            "image_url": c.image_url,
            "image_alt": c.image_alt,
            "summary": summary,
        } for c, summary, topic in content] if content else []

    def unread_content(self, user_id: str, topic_id: str) -> list[Dict] | None:
        print(
            f"Fetching unread content for user_id: {user_id}, topic_id: {topic_id}")

        content = (
            self.session.query(Content, Topic.title.label("topic"))
            .join(Topic, Content.topic_id == Topic.id)
            .outerjoin(UserFeedback, (UserFeedback.content_id == Content.id) & (UserFeedback.user_id == user_id))
            .filter(Content.topic_id == topic_id)
            .filter((UserFeedback.read.is_(None)) | (UserFeedback.read == False))
            .limit(1)
            .all()
        )

        print(f"Found {len(content) if content else 0} unread content")

        if not content or len(content) == 0:
            content = self.fetch_new_content(
                user_id=user_id,
                topic_id=topic_id
            )

        return [{
            "content_id": c.id,
            "topic_id": topic_id,
            "topic": topic,
            "title": c.title,
            "url": c.url,
            "favicon_url": c.favicon_url,
            "source": c.source,
            "image_url": c.image_url,
            "image_alt": c.image_alt
        } for c, topic in content] if content else []
