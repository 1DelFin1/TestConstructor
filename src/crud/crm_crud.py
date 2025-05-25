from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ResultModel, TestedUserModel


async def get_user_result(
    session: AsyncSession, test_id: int, email: str
) -> ResultModel:
    stmt = (
        select(ResultModel, TestedUserModel)
        .join(TestedUserModel)
        .where(ResultModel.test_id == test_id)
        .filter(TestedUserModel.email == email)
    )
    result = (await session.execute(stmt)).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Результат не найден, некорректный test_id или email",
        )
    return result[0]
