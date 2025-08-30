from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from core.utils import cuid


class Base(DeclarativeBase):
    id = Column(
        String(length=12),
        primary_key=True,
        index=True,
        default=lambda: cuid(12)
    )
    createdAt = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    updatedAt = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
