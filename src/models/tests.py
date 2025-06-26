from datetime import time
from uuid import UUID
from typing import TYPE_CHECKING, Union
from enum import Enum

from sqlalchemy import (
    String,
    ForeignKey,
    Boolean,
    Integer,
    Float,
    Time,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from src.models.users import UserModel, TestedUserModel


class QuestionTypes(Enum):
    single = "single"
    multiple = "multiple"
    text = "text"
    matching = "matching"


class TestModel(Base, TimestampMixin):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    passing_score: Mapped[int] = mapped_column(Float, nullable=False)
    duration: Mapped[time] = mapped_column(Time, nullable=False)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    author: Mapped["UserModel"] = relationship(
        back_populates="tests",
    )
    questions: Mapped[list["QuestionModel"]] = relationship(
        back_populates="test",
        cascade="all, delete-orphan",
        order_by="QuestionModel.id",
    )
    results: Mapped[list["ResultModel"]] = relationship(
        back_populates="test",
        cascade="all, delete-orphan",
        order_by="ResultModel.id",
    )


class QuestionModel(Base, TimestampMixin):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    question_type: Mapped[QuestionTypes] = mapped_column(nullable=False)
    scores: Mapped[int] = mapped_column(Integer, nullable=False)

    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
    )

    test: Mapped["TestModel"] = relationship(
        back_populates="questions",
    )
    options: Mapped[list["OptionModel"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="OptionModel.id",
    )


class OptionModel(Base, TimestampMixin):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    text: Mapped[str] = mapped_column(String(256), nullable=False)
    is_correct: Mapped[Union[bool, str]] = mapped_column(JSON, nullable=False)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    question: Mapped["QuestionModel"] = relationship(
        back_populates="options",
    )


class ResultModel(Base, TimestampMixin):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    score_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
    )
    tested_user_id: Mapped[int] = mapped_column(
        ForeignKey("tested_users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    test: Mapped["TestModel"] = relationship(
        "TestModel",
        back_populates="results",
        foreign_keys=[test_id],
    )
    tested_user: Mapped["TestedUserModel"] = relationship(
        "TestedUserModel",
        back_populates="result",
    )
