from functools import lru_cache
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class ConfigType:
    app_name: str = getenv('APP_NAME', 'Content Research Agent')
    tavily_api_key: str = getenv('TAVILY_API_KEY')
    jwt_secret: str = getenv('JWT_SECRET')
    gemini_api_key: str = getenv('GEMINI_API_KEY')
    gemini_model: str = getenv('GEMINI_MODEL')
    database_url: str = getenv('DATABASE_URL')
    content_per_topic: int = getenv('CONTENT_PER_TOPIC', 1)


@lru_cache
def get_config() -> ConfigType:
    return ConfigType()


Config = get_config()
