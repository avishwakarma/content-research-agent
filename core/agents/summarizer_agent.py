from google.adk import Agent
from config import Config


class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Summarizer_Agent",
            model=Config.gemini_model,
            description=(
                "Summarize content and extract key information for users."
            ),
            instruction=(
                "Your agent instructions goes here"
            ),
            tools=[
                # define tools needed
            ]
        )
