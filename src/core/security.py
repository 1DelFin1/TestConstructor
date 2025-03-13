from src.core.config import settings
from datetime import timedelta, datetime, timezone
from typing import Any
import jwt
from passlib.hash import pbkdf2_sha256


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)
