from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter

from src.schemas.editor import *
from src.core.database import engine, session_factory
from src.models.editor import *


router = APIRouter(
    prefix="/editor",
    tags=["editor"],
)


@router.post("")
async def add_editor(editor: EditorAddSchema):
    async with session_factory() as session:
        editor_one = EditorModel(username=editor.username, age=editor.age)
        session.add(editor_one)
        await session.commit()
    return {'response': True}


@router.get("")
async def get_editor():
    async with session_factory() as session:
        query = (
            select(EditorModel)
        )
        res = await session.execute(query)
        result = res.scalars().all()
    return {'response': result}


@router.post('/create_tables')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'response': True}
