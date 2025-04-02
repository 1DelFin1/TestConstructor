from typing import TYPE_CHECKING

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.tests import TestSchema
    from src.schemas.tested_users import TestedUserSchema


class ResultBaseSchema(TimestampSchema):
    score: float
    test_id: int
    tested_user_id: int
    score_passed: bool


class ResultCreateSchema(ResultBaseSchema):
    pass


class ResultOutSchema(ResultBaseSchema):
    id: int
    test: "TestSchema"
    tested_user: "TestedUserSchema"

    class Config:
        from_attributes = True


class ResultSchema(TimestampSchema):
    id: int
    score: float
    test_id: int
    tested_user_id: int
    score_passed: bool
    test: "TestSchema"
    tested_user: "TestedUserSchema"
