from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

from src.schemas.timestamp import TimestampSchema
from src.models.tests import QuestionTypes


if TYPE_CHECKING:
    from src.schemas.users import TestSchema
    from src.schemas.options import OptionSchema


class QuestionBaseSchema(TimestampSchema):
    title: str = Field(max_length=256)
    question_type: QuestionTypes
    scores: int
    test_id: int


class QuestionCreateSchema(QuestionBaseSchema):
    pass


class QuestionOutSchema(QuestionBaseSchema):
    id: int
    test: "TestSchema"
    options: list["OptionSchema"]

    class Config:
        from_attributes = True


class QuestionUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=256)
    question_type: QuestionTypes | None = None
    scores: int | None = None
    test_id: int | None = None


class QuestionSchema(TimestampSchema):
    id: int
    title: str = Field(max_length=256)
    question_type: QuestionTypes
    scores: int
    test_id: int
    test: "TestSchema"
    options: list["OptionSchema"]
