from typing import Annotated

from fastapi import HTTPException, status, Response, Depends

from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import verify_password
from src.crud import users_crud
from src.requset_forms import OAuth2EmailRequestForm


class JWTAuthenticator:
    @staticmethod
    def create_jwt_token(
        payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        if expire_timedelta:
            expire = datetime.utcnow() + expire_timedelta
        else:
            expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=datetime.utcnow(),
        )
        encoded = jwt.encode(to_encode, key, algorithm)
        return encoded

    @staticmethod
    def decode_jwt_token(
        token: str,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    ):
        return jwt.decode(token, key, algorithm)


class Authorization:
    @staticmethod
    async def login(
        session: AsyncSession,
        form_data: Annotated[OAuth2EmailRequestForm, Depends()],
        response: Response,
    ):
        user = await users_crud.get_user_by_email(session, form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email",
            )
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
        user_data = {
            "id": str(user.id),
            "username": user.email,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        token = JWTAuthenticator.create_jwt_token(user_data)
        response.set_cookie(
            key="token",
            value=token,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=True,
            secure=settings.IS_PROD,
            samesite="lax",
        )
