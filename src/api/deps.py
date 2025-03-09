from src.core.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from pydantic import ValidationError

from src.core.config import settings


async def get_db() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
