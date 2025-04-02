from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import EmailStr, Field

from src.schemas.timestamp import TimestampSchema


if TYPE_CHECKING:
    from src.schemas.tests import TestSchema


class UserBaseSchema(TimestampSchema):
    email: EmailStr = Field(max_length=255)
    first_name: str
    last_name: str
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(max_length=40)


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
