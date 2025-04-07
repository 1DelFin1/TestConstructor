from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import UserModel
from src.schemas import UserCreateSchema, UserUpdateSchema
from src.core.security import get_password_hash


async def create_user(
    session: AsyncSession, user: UserCreateSchema, is_superuser: bool = False
) -> UserModel:
    new_user = user.model_dump(exclude={"password"})
    new_user["hashed_password"] = get_password_hash(user.password)
    if is_superuser:
        new_user["is_superuser"] = True
    res_user = UserModel(**new_user)
    session.add(res_user)
    await session.commit()
    return res_user


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> UserModel | None:
    stmt = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.tests))
    )
    user = (await session.execute(stmt)).first()
    if not user:
        return None
    return user[0]


async def get_user_by_email(session: AsyncSession, email: str) -> UserModel | None:
    stmt = (
        select(UserModel)
        .where(UserModel.email == email)
        .options(selectinload(UserModel.tests))
    )
    result = await session.execute(stmt)
    if not result:
        return None
    user = result.first()
    if not user:
        return None
    return user[0]


async def get_users(session: AsyncSession):
    query = select(UserModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return result


async def update_user(
    session: AsyncSession, new_user: UserUpdateSchema, user_id: UUID
) -> UserModel | None:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None
    new_user_data = new_user.model_dump(exclude_unset=True)
    if "password" in new_user_data:
        password = new_user_data["password"]
        new_user_data["hashed_password"] = get_password_hash(password)
    for key, value in new_user_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: UUID) -> UserModel | None:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None
    await session.delete(user)
    await session.commit()
    return user
