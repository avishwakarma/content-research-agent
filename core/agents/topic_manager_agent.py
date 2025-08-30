
from google.adk import Agent
from config import Config


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
                "Your agent instructions goes here"
            ),
            tools=[
                # define tools needed
            ]
        )
