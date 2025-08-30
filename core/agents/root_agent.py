from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from config import Config

from .topic_manager_agent import TopicManagerAgent
from .content_manager_agent import ContentManagerAgent
from .summarizer_agent import SummarizerAgent


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
                "You are a strict orchestrator. Your ONLY job is to execute the following plan step-by-step. "
                "You MUST NOT use your own knowledge about any topic. Your entire operation depends on calling tools and using their exact output."

                "\n1. **GET Topic ID**: Your first and only action is to call the `cra_Topic_Manager_Agent` tool. "
                "Pass it the user's `user_id` and `topic` in a single text prompt."

                "\n2. **GET Content**: You MUST take the `topic_id` from the previous step's output. "
                "You are forbidden from proceeding if you did not get a valid `topic_id`. "
                "Call the `cra_Content_Manager_Agent` tool with the `user_id` and the received `topic_id`."

                "\n3. **SUMMARIZE Content**: You MUST take the list of content returned by the `ContentManagerAgent`. "
                "Call the `cra_Summarizer_Agent` tool with this list."

                "\n4. **FORMAT Final Output**: Your final task is to format the data you receive from the `SummarizerAgent`. "
                "**You are strictly forbidden from creating, inventing, or hallucinating any content, IDs, summaries, or keywords yourself.** "
                "Your final JSON response must be constructed **exclusively** from the data returned by the `SummarizerAgent` in the previous step. "
                "If the data from the previous step is empty, you MUST return a JSON object with an empty content list, like `{\"content\": []}`."
            ),
            model=Config.gemini_model,
            tools=[
                AgentTool(agent=TopicManagerAgent()),
                AgentTool(agent=ContentManagerAgent()),
                AgentTool(agent=SummarizerAgent()),
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
