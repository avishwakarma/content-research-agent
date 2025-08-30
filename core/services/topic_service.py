from core.database import session
from core.models import Topic, UserTopic


class TopicService:
    def __init__(self):
        self.session = session

    def get_user_topics(self, user_id: str):
        return (
            self.session.query(Topic)
            .join(UserTopic, UserTopic.topic_id == Topic.id)
            .filter(UserTopic.user_id == user_id)
            .all()
        )

    def user_topic(self, user_id: str, topic: str):

        print(f"Looking for topic '{topic}' for user_id: {user_id}")

        instance = (
            self.session.query(UserTopic)
            .join(Topic, UserTopic.topic_id == Topic.id)
            .filter(UserTopic.user_id == user_id, Topic.title == topic)
            .first()
        )

        if not instance:
            topic = self.add_topic(topic)
            instance = UserTopic(user_id=user_id, topic_id=topic.id)
            self.session.add(instance)
            self.session.commit()

        print(f"UserTopic instance: {instance}")

        return {
            "id": instance.id,
            "user_id": instance.user_id,
            "topic_id": instance.topic_id
        }

    def add_topic(self, topic: str):
        topic = Topic(title=topic)
        self.session.add(topic)
        self.session.commit()
        return topic
