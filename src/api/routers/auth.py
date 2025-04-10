from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from src.api.deps import SessionDep
from src.api.jwt_utils import JWTAuthenticator
from src.crud import users_crud
from src.core.security import verify_password
from src.core.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
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
    return {"message": "Logged is successfully"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"message": "Successfully logged out"}
