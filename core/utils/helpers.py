from urllib.parse import urlparse
from bcrypt import hashpw, gensalt, checkpw
from fastapi.responses import JSONResponse
from fastapi import status
import re
import json


def source_from_url(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    parts = hostname.split(".")

    if len(parts) >= 2:
        return parts[-2]

    return hostname


def to_hash(text: str) -> str:
    return hashpw(text.encode("utf-8"), gensalt()).decode("utf-8")


def compare_hash(text: str, hashed: str) -> bool:
    return checkpw(text.encode("utf-8"), hashed.encode("utf-8"))


def text_to_json(content: str) -> JSONResponse:
    if not content or len(content.strip()) == 0:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Agent produced empty response."
            }
        )

    match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)

    if match:
        content = match.group(1)

    try:
        parsed_json = json.loads(content)
        return parsed_json

    except json.JSONDecodeError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Agent produced malformed JSON.",
                "details": content
            }
        )
