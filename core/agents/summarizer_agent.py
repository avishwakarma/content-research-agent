from google.adk import Agent
from google.adk.tools import FunctionTool
from config import Config
from core.services import ContentService
from core.tools import Summarizer

contentService = ContentService()
summarizer = Summarizer()


def summarize_content(content_id: str, user_id: str):
    print(f"Summarizing content_id: {content_id} for user_id: {user_id}")

    user_summary = contentService.get_user_summary(content_id, user_id)

    print(
        f"User summary for content_id: {content_id} and user_id: {user_id} is: {user_summary}")

    if user_summary:
        return user_summary

    raw_content = contentService.get_content_by_id(content_id)['raw_content']
    summary = summarizer.summarize(raw_content)
    print(f"Generated summary for content_id: {content_id}: {summary}")
    contentService.add_summary(
        content_id=content_id, summary=summary, user_id=user_id)
    print(f"Saved summary for content_id: {content_id} and user_id: {user_id}")


get_final_content_list = FunctionTool(
    func=contentService.get_content_by_ids,
)

do_summary = FunctionTool(
    func=summarize_content,
)


class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="cra_Summarizer_Agent",
            model=Config.gemini_model,
            description=(
                "Summarize content and extract key information for users."
            ),
            instruction=(
                "You are a specialist summarization agent. You will receive a `user_id` and a `content_list` containing lightweight content metadata (like `content_id`)."
                "\nYour mission is to ensure every item in this list has a summary by calling your tools."

                "\n**For EACH item in the `content_list`, you must do the following:**"
                "\n1. **Call `do_summary`**: You have a powerful tool called `do_summary`. Call this tool **exactly once** for each item. Pass the item's `content_id` and the `user_id`."

                "\n**Final Step (After the loop is complete):**"
                "\n2. Once you have called `do_summary` for all items, call the `get_final_content_list` tool. Pass it the `user_id` and the complete list of all `content_ids` you were originally given."
                "\n3. Your final response MUST be the direct output from the `get_final_content_list` tool."
            ),
            tools=[
                do_summary,
                get_final_content_list
            ]
        )
