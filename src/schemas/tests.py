from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, Field

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.users import UserSchema
    from src.schemas.questions import QuestionSchema
    from src.schemas.results import ResultSchema


class TestBaseSchema(TimestampSchema):
    title: str = Field(max_length=256)
    description: str = Field(max_length=256)
    user_id: UUID


class TestCreateSchema(TestBaseSchema):
    pass


class TestOutSchema(TestBaseSchema):
    id: int
    author: "UserSchema"
    questions: list["QuestionSchema"]
    results: list["ResultSchema"]

    class Config:
        from_attributes = True


class TestUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=256)
    description: str | None = Field(default=None, max_length=256)
    user_id: UUID | None = None


class TestSchema(TimestampSchema):
    id: int
    title: str
    description: str
    user_id: UUID
    author: "UserSchema"
    questions: list["QuestionSchema"]
    results: list["ResultSchema"]
