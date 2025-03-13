from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from src.schemas import TestSchema


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
