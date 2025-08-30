from google.adk import Agent
from config import Config


class ContentManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Content_Manager_Agent",
            model=Config.gemini_model,
            description=(
                "Manage content based on the topic_id and user_id."
            ),
            instruction=(
                "Your agent instructions goes here"
            ),
            tools=[
                # define tools needed
            ],
        )
