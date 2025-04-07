from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from sqlalchemy.orm import selectinload, joinedload

from src.models import UserModel, ResultModel, TestedUserModel
from src.schemas import UserCreateSchema
from src.core.security import get_password_hash


async def get_user_result(
    session: AsyncSession, test_id: int, email: str
) -> ResultModel | None:
    stmt = (
        select(ResultModel)
        .join(TestedUserModel)
        .where(ResultModel.test_id == test_id and TestedUserModel.email == email)
    )
    result = (await session.execute(stmt)).first()
    if not result:
        return None
    return result[0]
