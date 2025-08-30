from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from config import Config


class RootAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            name="cra_Root_Agent",
            description=(
                "Analyze topics provided by the users, "
                "generate relevant content based on their needs, "
                "and manage the overall conversation flow."
            ),
            instruction=(
                'For each user query, return a simple message \'{"message": "Hello World"}\''
            ),
            model=Config.gemini_model,
            tools=[
                # define tools needed
            ],
        )


async def run_root(topic: str, user_id: str):

    session_service = InMemorySessionService()
    await session_service.create_session(app_name=Config.app_name, user_id=user_id, session_id=user_id)

    runner = Runner(
        agent=RootAgent(),
        session_service=session_service,
        app_name=Config.app_name
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"user_id: {user_id}\ntopic: {topic}"
            )
        ]
    )

    events = runner.run(
        user_id=user_id,
        session_id=user_id,
        new_message=content
    )

    final_event = None

    for event in events:
        print("--- AGENT EVENT ---")
        print(event)

        if event.author == "cra_Root_Agent" and event.content and event.content.role == "model":
            final_event = event

    if final_event and final_event.content and final_event.content.parts:
        return final_event.content.parts[0].text
