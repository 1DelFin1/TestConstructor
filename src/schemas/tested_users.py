from typing import TYPE_CHECKING
from pydantic import EmailStr, Field

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.tests import TestSchema


class TestedUserBaseSchema(TimestampSchema):
    email: EmailStr = Field(max_length=255)
    first_name: str
    last_name: str
    score: int


class TestedUserCreateSchema(TestedUserBaseSchema):
    pass


class TestedUserOutSchema(TestedUserBaseSchema):
    id: int
    result: "TestSchema"

    class Config:
        from_attributes = True


class TestedUserSchema(TestedUserCreateSchema):
    id: int
    email: str
    first_name: str
    last_name: str
    result: "TestSchema"
