from fastapi import APIRouter, Query, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from uuid import UUID

from src.api.deps import SessionDep
from src.core.database import engine, session_factory, Base
from src.core.security import get_password_hash
from src.crud import users_crud, tests_crud
from src.schemas import UserCreateSchema, TestCreateSchema
from src.models import TestModel, UserModel


router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@router.post("/create_or_save_test")
async def create_test(
    session: SessionDep, test: TestCreateSchema, test_id: int | None = None
):
    test = await tests_crud.create_or_save_test(session, test, test_id)
    return test


@router.get("/get_test/{test_id}")
async def get_test(session: SessionDep, test_id: int):
    test = await tests_crud.get_test_by_id(session, test_id)
    return test


@router.delete("/delete_test/{test_id}")
async def delete_test(session: SessionDep, test_id: int):
    test = await tests_crud.delete_test(session, test_id)
    return test
