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


class UserAddSchema(BaseModel):
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


class UserSchema(UserAddSchema):
    id: UUID
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

