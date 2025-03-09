from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings


engine = create_async_engine(str(settings.POSTGRES_URL_ADDRESS), echo=True)


class Base(DeclarativeBase):
    pass
