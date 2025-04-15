from fastapi import APIRouter

from src.api.deps import SessionDep
from src.crud import tests_crud
from src.schemas import (
    TestCreateSchema,
    TestSendSchema,
    TestedUserCreateSchema,
)


router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@router.post("/create_or_save_test")
async def create_or_save_test(
    session: SessionDep, test: TestCreateSchema, test_id: int | None = None
):
    test = await tests_crud.create_or_save_test(session, test, test_id)
    return test


@router.get("/get_test/{test_id}")
async def get_test(session: SessionDep, test_id: int):
    test = await tests_crud.get_test_by_id(session, test_id)
    return test


@router.post("/send_test")
async def send_test(
    session: SessionDep,
    test_id: int,
    test: TestSendSchema,
    tested_user: TestedUserCreateSchema,
):
    result = await tests_crud.send_test(session, test_id, test, tested_user)
    return result


@router.delete("/delete_test/{test_id}")
async def delete_test(session: SessionDep, test_id: int):
    test = await tests_crud.delete_test(session, test_id)
    return test
