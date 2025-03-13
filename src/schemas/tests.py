from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from src.schemas import UserSchema


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
