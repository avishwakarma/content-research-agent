from google.adk.tools import FunctionTool
from google.adk import Agent
from core.services.topic_service import TopicService
from config import Config

topicService = TopicService()

get_topic = FunctionTool(
    func=topicService.user_topic,
)


class TopicManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Topic_Manager_Agent",
            model=Config.gemini_model,
            description=(
                "Manages the user's topic. "
                "Maps topic with user_id and topic_id."
            ),
            instruction=(
                "Your sole purpose is to get user topic. Follow this exact, short plan:"
                "\n1. **Parse Input**: Extract the `user_id` and `topic` from the incoming text."
                "\n2. **Call Tool Once**: Call the `get_topic` tool **exactly one time** with the parsed arguments."
                "\n3. **Return and Stop**: The `topic_id` and `user_id` are your **final answer**."
            ),
            tools=[
                get_topic
            ]

        )
