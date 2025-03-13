from datetime import datetime
import enum
from uuid import uuid4, UUID
from typing import Annotated, Optional
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    func,
    text,
    DATETIME,
    CheckConstraint,
    CheckConstraint,
    UniqueConstraint,
    Index,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )


class UserModel(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    first_name: Mapped[String] = mapped_column(String(255), nullable=False)
    last_name: Mapped[String] = mapped_column(String(255), nullable=False)
    username: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    tests: Mapped[list["TestModel"]] = relationship(
        back_populates="author",
    )


class TestModel(Base, TimestampMixin):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["UserModel"] = relationship(
        back_populates="tests",
    )
