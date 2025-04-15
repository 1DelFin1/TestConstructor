from typing import Annotated
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.jwt_utils import JWTAuthenticator
from src.crud import users_crud
from src.core.security import verify_password
from src.core.database import engine
from src.schemas import UserCreateSchema, TokenSchema, UserInDBSchema


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


# Headers

# async def get_current_token_payload(
#     token: str = Depends(oauth2_scheme),
# ):
#     try:
#         payload = JWTAuthenticator.decode_jwt_token(token)
#     except InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
#         )
#     return payload
#
#
# async def get_current_auth_user(
#     session: SessionDep,
#     payload: dict = Depends(get_current_token_payload),
# ):
#     email = payload.get("email")
#     user = await users_crud.get_user_by_email(session, email)
#     if user:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="User not found",
#     )


# async def get_current_active_auth_user(
#     current_user: UserCreateSchema = Depends(get_current_auth_user),
# ):
#
#     if current_user.is_active:
#         return current_user
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Inactive user",
#     )


# Cookies


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
