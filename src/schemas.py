from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime

from src.models.tests import QuestionTypes


# Timestamp
class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


# User
class UserBaseSchema(TimestampSchema):
    email: EmailStr = Field(max_length=255)
    first_name: str
    last_name: str
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(max_length=40)


class UserUpdateSchema(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    password: str | None = None


class UserOutSchema(UserBaseSchema):
    id: UUID

    class Config:
        from_attributes = True


class UserInDBSchema(UserBaseSchema):
    id: UUID
    hashed_password: str


class UserSchema(TimestampSchema):
    id: UUID
    email: str
    first_name: str
    last_name: str
    username: str | None
    hashed_password: str
    is_active: bool
    is_superuser: bool = False
    tests: list["TestSchema"]


# Test
class TestBaseSchema(TimestampSchema):
    title: str = Field(max_length=256)
    description: str = Field(max_length=256)
    user_id: UUID
    passing_score: float


class TestCreateSchema(TestBaseSchema):
    # author: "UserSchema"
    questions: list["QuestionCreateSchema"]


class TestOutSchema(TestBaseSchema):
    id: int
    # author: "UserSchema"
    questions: list["QuestionSchema"] | None
    results: list["ResultSchema"] | None

    class Config:
        from_attributes = True


class TestUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=256)
    description: str | None = Field(default=None, max_length=256)
    passing_score: float | None = None


class TestSchema(TimestampSchema):
    id: int
    title: str
    description: str
    user_id: UUID
    passing_score: float
    # author: "UserSchema"
    questions: list["QuestionSchema"]
    results: list["ResultSchema"]


# Question
class QuestionBaseSchema(TimestampSchema):
    title: str = Field(max_length=256)
    question_type: "QuestionTypes"
    scores: int
    test_id: int


class QuestionCreateSchema(QuestionBaseSchema):
    # test: "TestSchema"
    options: list["OptionCreateSchema"]


class QuestionOutSchema(QuestionBaseSchema):
    id: int
    # test: "TestSchema"
    options: list["OptionSchema"]

    class Config:
        from_attributes = True


class QuestionUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=256)
    question_type: QuestionTypes | None = None
    scores: int | None = None


class QuestionSchema(TimestampSchema):
    id: int
    title: str = Field(max_length=256)
    question_type: "QuestionTypes"
    scores: int
    test_id: int
    # test: "TestSchema"
    options: list["OptionSchema"]


# Option
class OptionBaseSchema(TimestampSchema):
    text: str = Field(max_length=256)
    is_correct: bool
    question_id: int


class OptionCreateSchema(OptionBaseSchema):
    pass
    # question: "QuestionSchema"


class OptionOutSchema(OptionBaseSchema):
    id: int
    question: "QuestionSchema"

    class Config:
        from_attributes = True


class OptionUpdateSchema(BaseModel):
    text: str | None = Field(default=None, max_length=256)
    is_correct: bool | None = None


class OptionSchema(TimestampSchema):
    id: int
    text: str = Field(max_length=256)
    is_correct: bool
    question_id: int
    question: "QuestionSchema"


# Result
class ResultBaseSchema(TimestampSchema):
    score: float
    score_passed: bool
    test_id: int
    tested_user_id: int


class ResultCreateSchema(ResultBaseSchema):
    # test: "TestSchema"
    # tested_user: "TestedUserSchema"
    pass


class ResultOutSchema(ResultBaseSchema):
    id: int
    # test: "TestSchema"
    # tested_user: "TestedUserSchema"

    class Config:
        from_attributes = True


class ResultSchema(TimestampSchema):
    id: int
    score: float
    test_id: int
    tested_user_id: int
    score_passed: bool
    # test: "TestSchema"
    # tested_user: "TestedUserSchema"


# Tested user
class TestedUserBaseSchema(TimestampSchema):
    email: EmailStr = Field(max_length=255)
    first_name: str
    last_name: str
    score: int


class TestedUserCreateSchema(TestedUserBaseSchema):
    pass


class TestedUserOutSchema(TestedUserBaseSchema):
    id: int
    result: "ResultSchema"

    class Config:
        from_attributes = True


class TestedUserSchema(TimestampSchema):
    id: int
    email: str
    first_name: str
    last_name: str
    result: "ResultSchema"


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
