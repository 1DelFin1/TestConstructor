from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional

from src.models import TimestampMixin


class EditorAddSchema(BaseModel):
    username: str
    age: int


class EditorSchema(EditorAddSchema):
    id: int


class TimestampSchema(BaseModel):
    # created_at: datetime
    # updated_at: datetime
    pass


class UserBaseSchema(BaseModel):
    email: EmailStr = Field(max_length=255)
    first_name: str
    last_name: str
    is_active: bool = True
    is_superuser: bool = False
    role: str
    username: str | None = Field(default=None, max_length=255)


class UserAddSchema(UserBaseSchema):
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
    role: str
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    tests: list["TestSchema"]


class TestAddSchema(BaseModel):
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class TestSchema(TimestampSchema):
    id: UUID
    author: UserSchema

