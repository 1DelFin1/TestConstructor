from fastapi import APIRouter, HTTPException, status, Depends

from uuid import UUID

from src.api.deps import SessionDep, get_current_active_auth_user
from src.crud import users_crud
from src.models.users import UserModel
from src.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserInDBSchema,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/users/me")
async def get_current_user(
    current_user: UserInDBSchema = Depends(get_current_active_auth_user),
):
    return current_user  # поменять на dict


@router.post("/create_user")
async def create_user(
    session: SessionDep, user_create: UserCreateSchema, is_superuser: bool | None = None
):
    user = await users_crud.get_user_by_email(session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже создан",
        )
    user = await users_crud.create_user(session, user_create, is_superuser)
    return user


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
async def delete_user(session: SessionDep, user_id: UUID):
    result = await users_crud.delete_user(session, user_id)
    return result
