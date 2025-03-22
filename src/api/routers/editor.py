from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Query, Depends, HTTPException, status

from src.core.security import get_password_hash
from src.api.deps import SessionDep
from src.core.database import engine, session_factory, Base
from src.schemas import (
    UserCreateSchema,
    UserInDBSchema,
    UserOutSchema,
    TestOutSchema,
    TestCreateSchema,
)
from src.models import TestModel, UserModel


router = APIRouter(
    prefix="/editor",
    tags=["editor"],
)


@router.post("/create_user")
async def create_user(user: UserCreateSchema, session: SessionDep):
    new_user = user.model_dump(exclude={"password"})
    new_user["hashed_password"] = get_password_hash(user.password)
    res_user = UserModel(**new_user)
    session.add(res_user)
    await session.commit()
    return {"response": True}


@router.get("/get_users")
async def get_users(session: SessionDep):
    query = select(UserModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return {"response": result}


@router.post("/create_test")
async def create_test(test: TestCreateSchema, session: SessionDep):
    new_test = test.model_dump()
    us = TestModel(**new_test)
    session.add(us)
    await session.commit()
    return {"response": True}


@router.get("/get_tests")
async def get_tests(session: SessionDep):
    query = select(TestModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return {"response": result}
