from uuid import UUID

from fastapi import APIRouter

from src.api.deps import SessionDep
from src.crud import tests_crud
from src.schemas import (
    TestCreateSchema,
)


router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@router.post("")
async def create_or_save_test(
    session: SessionDep, test: TestCreateSchema, test_id: int | None = None
):
    test = await tests_crud.create_or_save_test(session, test, test_id)
    return test


@router.get("/{test_id}")
async def get_test(session: SessionDep, test_id: int):
    test = await tests_crud.get_test_by_id(session, test_id)
    return test


@router.get("/user/{user_id}")
async def get_user_tests(session: SessionDep, user_id: UUID):
    tests = await tests_crud.get_user_tests(session, user_id)
    return tests


@router.get("/users/{test_id}")
async def get_users_sent(session: SessionDep, test_id: int):
    tests = await tests_crud.get_users_sent(session, test_id)
    return {"test": tests, "ok": True}


@router.delete("/{test_id}")
async def delete_test(session: SessionDep, test_id: int):
    test = await tests_crud.delete_test(session, test_id)
    return test
