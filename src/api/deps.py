from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from jwt.exceptions import InvalidTokenError

from src.api.utils import JWTAuthenticator
from src.crud import users_crud
from src.core.database import engine


async def get_db() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_active_auth_user(request: Request, session: SessionDep):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    try:
        payload = JWTAuthenticator.decode_jwt_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await users_crud.get_user_by_email(session, payload.get("email"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
