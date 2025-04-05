from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.questions import QuestionSchema


class OptionBaseSchema(TimestampSchema):
    text: str = Field(max_length=256)
    is_correct: bool
    question_id: int


class OptionCreateSchema(OptionBaseSchema):
    pass


class OptionOutSchema(OptionBaseSchema):
    id: int
    question: "QuestionSchema"

    class Config:
        from_attributes = True


class OptionUpdateSchema(BaseModel):
    text: str | None = Field(default=None, max_length=256)
    is_correct: bool | None = None
    question_id: int | None = None


class OptionSchema(TimestampSchema):
    id: int
    text: str = Field(max_length=256)
    is_correct: bool
    question_id: int
    question: "QuestionSchema"


# OptionBaseSchema.model_rebuild()
# OptionCreateSchema.model_rebuild()
# OptionOutSchema.model_rebuild()
# OptionUpdateSchema.model_rebuild()
# OptionSchema.model_rebuild()
