from google.adk import Agent
from google.adk.tools import FunctionTool
from config import Config
from core.services import ContentService

contentService = ContentService()

get_unread_content = FunctionTool(
    func=contentService.unread_content,
)


class ContentManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Content_Manager_Agent",
            model=Config.gemini_model,
            description=(
                "Manage content based on the topic_id and user_id."
            ),
            instruction=(
                "Your sole purpose is to fetch a list of unread content. You will receive a text prompt with a `user_id` and a `topic_id`. Follow this exact, short plan:"
                "\n1. **Parse Input**: Extract the `user_id` and `topic_id` from the incoming text."
                "\n2. **Call Tool Once**: Call the `get_unread_content` tool **exactly one time** with the parsed arguments."
                "\n3. **Return and Stop**: The list of content returned by the tool is your **final answer**. You must immediately return this list as your output and then stop all further actions. Do not repeat the process or call the tool again."
            ),
            tools=[
                get_unread_content
            ],
        )
