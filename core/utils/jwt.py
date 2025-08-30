from fastapi import Request
import jwt
import datetime
from typing import Any, Dict
from config import Config


class Jwt:
    @staticmethod
    def generate(payload: Dict[str, Any], expires_in: int = 3600) -> str:
        payload_copy = payload.copy()

        payload_copy['exp'] = datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=expires_in)

        token = jwt.encode(
            payload_copy, Config.jwt_secret, algorithm='HS256')

        return token

    @staticmethod
    def verify(token: str) -> Dict[str, Any] | None:
        try:
            payload = jwt.decode(
                token,
                Config.jwt_secret,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
