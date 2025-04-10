from datetime import datetime, timedelta
import jwt

from src.core.config import settings


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
        encoded = jwt.encode(payload, key, algorithm)
        return encoded

    @staticmethod
    def decode_jwt_token(
        token: str,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    ):
        return jwt.decode(token, key, algorithm)
