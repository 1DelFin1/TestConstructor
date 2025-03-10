from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Query, Depends, HTTPException, status

from src.api.deps import SessionDep
from src.core.database import engine, session_factory, Base
from src.schemas import EditorAddSchema, EditorSchema, UserSchema, UserAddSchema, TestAddSchema, UserInDBSchema
from src.models import EditorModel, TestModel, UserModel


router = APIRouter(
    prefix="/editor",
    tags=["editor"],
)


@router.post('/create_user')
async def create_user(user: UserInDBSchema, session: SessionDep):
    new_user = user.model_dump()
    us = UserModel(**new_user)
    session.add(us)
    await session.commit()
    return {'response': True}


@router.get('/get_users')
async def get_users(session: SessionDep):
    query = select(UserModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return {'response': result}


@router.post('/create_test')
async def create_test(test: TestAddSchema, session: SessionDep):
    new_test = test.model_dump()
    us = TestModel(**new_test)
    session.add(us)
    await session.commit()
    return {'response': True}


@router.get('/get_tests')
async def get_tests(session: SessionDep):
    query = select(TestModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return {'response': result}


@router.post("")
async def add_editor(editor: EditorAddSchema, session: SessionDep):
    editor_one = EditorModel(username=editor.username, age=editor.age)
    print(editor_one)
    session.add(editor_one)
    await session.commit()
    return {'response': True}


@router.get("")
async def get_editor(session: SessionDep):
    query = select(EditorModel)
    res = await session.execute(query)
    result = res.scalars().all()
    return {'response': result}


@router.post('/create_tables')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'response': True}
