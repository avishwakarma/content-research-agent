from core.database import session
from core.models import User
from core.utils import Jwt, to_hash, compare_hash


class AuthService:
    def __init__(self):
        self.jwt = Jwt()
        self.session = session

    def register(self, user_data: dict) -> str:
        user = User(**user_data)

        user.password = to_hash(user.password)

        self.session.add(user)
        self.session.commit()

        payloadUser = {"id": user.id, "email": user.email, "name": user.name}

        return {
            "token": self.jwt.generate(payloadUser),
            "refresh_token": self.jwt.generate(payloadUser, expires_in=86400),
            "user": payloadUser
        }

    def login(self, email: str, password: str) -> str | None:
        user = self.session.query(User).filter_by(email=email).first()

        if not user:
            return ValueError("User not found")

        if not compare_hash(password, user.password):
            return ValueError("Invalid password")

        payloadUser = {"id": user.id, "email": user.email, "name": user.name}

        return {
            "token": self.jwt.generate(payloadUser),
            "refresh_token": self.jwt.generate(payloadUser, expires_in=86400),
            "user": payloadUser
        }
