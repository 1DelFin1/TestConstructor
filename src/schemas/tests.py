from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


if TYPE_CHECKING:
    from src.schemas.users import UserSchema


class TestBaseSchema(BaseModel):
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class TestAddSchema(TestBaseSchema):
    pass


class TestOutSchema(TestBaseSchema):
    id: UUID


class TestSchema(TestBaseSchema):
    id: UUID
    author: "UserSchema"
