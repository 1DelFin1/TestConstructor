from uuid import uuid4, UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.users import TimestampMixin


if TYPE_CHECKING:
    from src.models.users import UserModel


class TestModel(Base, TimestampMixin):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["UserModel"] = relationship(
        back_populates="tests",
    )
