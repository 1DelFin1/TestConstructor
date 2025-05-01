from uuid import UUID

from fastapi import APIRouter

from src.api.utils import get_users_score
from src.api.sending_result import send_result_on_email
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


@router.get("/get_user_tests/{user_id}")
async def get_user_tests(session: SessionDep, user_id: UUID):
    tests = await tests_crud.get_user_tests(session, user_id)
    return tests


@router.post("/send_test")
async def send_test(
    session: SessionDep,
    test_id: int,
    test: TestSendSchema,
    tested_user: TestedUserCreateSchema,
):
    result = await tests_crud.send_test(session, test_id, test, tested_user)
    score_is_passed, users_score = await get_users_score(session, tested_user)
    await send_result_on_email(
        tested_user.email,
        test.title,
        users_score,
        score_is_passed,
        test.passing_score,
    )
    return result


@router.delete("/delete_test/{test_id}")
async def delete_test(session: SessionDep, test_id: int):
    test = await tests_crud.delete_test(session, test_id)
    return test
