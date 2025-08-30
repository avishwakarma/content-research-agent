from sqlalchemy import Column, String, Date
from .base_model import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    dob = Column(Date, nullable=True)
