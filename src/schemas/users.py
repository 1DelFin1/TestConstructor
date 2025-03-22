from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from datetime import datetime


if TYPE_CHECKING:
    from src.schemas.tests import TestSchema


class UserBaseSchema(BaseModel):
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


class UserSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    username: str | None
    hashed_password: str
    is_active: bool
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    tests: list["TestSchema"]
