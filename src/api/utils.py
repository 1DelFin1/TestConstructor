from typing import Annotated

from fastapi import HTTPException, status, Response, Depends

from datetime import datetime, timedelta
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.config import settings
from src.core.security import verify_password
from src.crud import users_crud
from src.models import QuestionTypes, TestedUserModel, ResultModel
from src.requset_forms import OAuth2EmailRequestForm
from src.schemas import TestedUserCreateSchema


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
        incorrect_user_data_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
        if not user:
            raise incorrect_user_data_exception
        if not verify_password(form_data.password, user.hashed_password):
            raise incorrect_user_data_exception
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
            httponly=False,  # изменить на True
            secure=settings.IS_PROD,
            samesite="lax",
        )


class CheckAnswers:
    def __init__(
        self,
        score,
        current_question_score,
        question_type,
        right_options,
        user_options,
        user_answer_text,
    ):
        self.score = score
        self.current_question_score = current_question_score
        self.question_type = question_type
        self.right_options = right_options
        self.user_options = user_options
        self.user_answer_text = user_answer_text

    async def check_single_type(self):
        user_selected = next(
            (opt for opt in self.user_options if opt.get("is_correct", False)), None
        )
        if user_selected and any(
            opt["text"] == user_selected["text"] and opt["is_correct"]
            for opt in self.right_options
        ):
            self.score += self.current_question_score

    async def check_multiple_and_pair_type(self):
        correct_set = {opt["text"] for opt in self.right_options if opt["is_correct"]}
        user_set = {
            opt["text"] for opt in self.user_options if opt.get("is_correct", False)
        }
        if correct_set == user_set:
            self.score += self.current_question_score

    async def check_text_type(self):
        if self.user_answer_text:
            self.score += self.current_question_score

    async def check_answer(self):
        if self.question_type == QuestionTypes.single:
            await self.check_single_type()

        elif (
            self.question_type == QuestionTypes.multiple
            or self.question_type == QuestionTypes.matching
        ):
            await self.check_multiple_and_pair_type()

        elif self.question_type == QuestionTypes.text:
            await self.check_text_type()


async def get_users_score(
    session: AsyncSession,
    tested_user: TestedUserCreateSchema,
    test_id: int,
):
    stmt = (
        select(ResultModel, TestedUserModel)
        .join(TestedUserModel)
        .where(TestedUserModel.id == ResultModel.tested_user_id)
        .filter(TestedUserModel.email == tested_user.email)
        .filter(ResultModel.test_id == test_id)
    )
    tested_user_model = await session.scalar(stmt)
    return tested_user_model.score
