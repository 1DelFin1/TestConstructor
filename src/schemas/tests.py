from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, Field

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.users import UserSchema
    from src.schemas.questions import QuestionSchema, QuestionCreateSchema
    from src.schemas.results import ResultSchema


class TestBaseSchema(TimestampSchema):
    title: str = Field(max_length=256)
    description: str = Field(max_length=256)
    user_id: UUID
    passing_score: float


class TestCreateSchema(TestBaseSchema):
    # pass
    author: "UserSchema"
    questions: list["QuestionCreateSchema"]


class TestOutSchema(TestBaseSchema):
    id: int
    author: "UserSchema"
    questions: list["QuestionSchema"] | None
    results: list["ResultSchema"] | None

    class Config:
        from_attributes = True


class TestUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=256)
    description: str | None = Field(default=None, max_length=256)
    user_id: UUID | None = None
    passing_score: float | None = None


class TestSchema(TimestampSchema):
    id: int
    title: str
    description: str
    user_id: UUID
    passing_score: float
    author: "UserSchema"
    questions: list["QuestionSchema"]
    results: list["ResultSchema"]


# TestBaseSchema.model_rebuild()
# TestCreateSchema.model_rebuild()
# TestOutSchema.model_rebuild()
# TestUpdateSchema.model_rebuild()
# TestSchema.model_rebuild()
