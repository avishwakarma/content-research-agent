from google.adk import Agent
from config import Config


class ContentRankingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Content_Ranking_Agent",
            model=Config.gemini_model,
            description=(
                "Rank content based on relevance and user preferences."
            ),
            tools=[
            ],
        )
