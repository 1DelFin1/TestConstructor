from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, DATETIME, CheckConstraint, CheckConstraint, UniqueConstraint, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from src.core.database import Base



