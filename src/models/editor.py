from datetime import datetime
import enum

from typing import Annotated, Optional
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, DATETIME, CheckConstraint, CheckConstraint, UniqueConstraint, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class EditorModel(Base):
    __tablename__ = 'editor'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    age: Mapped[int]
