from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class EditorAddSchema(BaseModel):
    username: str
    age: int


class EditorSchema(EditorAddSchema):
    id: int
