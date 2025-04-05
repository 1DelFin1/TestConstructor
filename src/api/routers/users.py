from fastapi import APIRouter, Query, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from uuid import UUID

from src.api.deps import SessionDep
from src.core.database import engine, session_factory, Base
from src.core.security import get_password_hash
from src.crud import users_crud
from src.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    TestCreateSchema,
)
from src.models import TestModel, UserModel


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create_user")
async def create_user(
    session: SessionDep, user_create: UserCreateSchema, is_superuser: bool | None = None
) -> dict:
    user = await users_crud.get_user_by_email(session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже создан",
        )
    user = await users_crud.create_user(session, user_create, is_superuser)
    return {"response": True}


@router.get("/get_users")
async def get_users(session: SessionDep):
    users = await users_crud.get_users(session)
    return users


@router.get("/get_users/{user_id}")
async def get_user(session: SessionDep, user_id: UUID):
    result = await users_crud.get_user_by_id(session, user_id)
    return result


@router.post("/update_user/{user_id}")
async def update_user(session: SessionDep, new_user: UserUpdateSchema, user_id: UUID):
    result = await users_crud.update_user(session, new_user, user_id)
    return result


@router.delete("/delete_user/{user_id}")
async def update_user(session: SessionDep, user_id: UUID):
    result = await users_crud.delete_user(session, user_id)
    return result
