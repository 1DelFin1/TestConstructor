from fastapi import APIRouter, Query, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from src.api.deps import SessionDep
from src.core.database import engine, session_factory, Base
from src.core.security import get_password_hash
from src.crud import crm_crud
from src.models import TestModel, UserModel
from src.schemas import UserCreateSchema


router = APIRouter(
    prefix="/crm",
    tags=["crm"],
)


@router.get("/")
async def get_result(session: SessionDep, test_id: int, email: str):
    result = await crm_crud.get_user_result(session, test_id, email)
    return result
