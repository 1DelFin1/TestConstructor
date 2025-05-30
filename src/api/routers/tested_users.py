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
    prefix="/tested_users",
    tags=["tested_users"],
)


@router.post("/send_test")
async def send_test(
    session: SessionDep,
    test_id: int,
    test: TestSendSchema,
    tested_user: TestedUserCreateSchema,
):
    result = await tests_crud.send_test(session, test_id, test, tested_user)
    users_score = await get_users_score(session, tested_user, test_id)
    await send_result_on_email(
        tested_user.email,
        test.title,
        users_score,
        test.passing_score,
    )
    return result
