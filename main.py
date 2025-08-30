from uvicorn import run
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from config import Config
from core.agents import run_root
from core.services import AuthService
from core.utils import text_to_json

app = FastAPI(
    title=Config.app_name,
    description="An AI agent to assist users in researching and generating content based on specified topics."
)


@app.post('/register')
async def register_user(request: Request):
    user_data = await request.json()
    auth = AuthService()
    return auth.register(user_data)


@app.get("/")
async def main(request: Request):
    topic = request.query_params.get("topic")
    user_id = request.query_params.get("user_id")

    if not topic or not user_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Both 'topic' and 'user_id' query parameters are required."
            }
        )

    print(f"Received topic: {topic} for user_id: {user_id}")
    content = await run_root(topic=topic, user_id=user_id)

    return text_to_json(content)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
