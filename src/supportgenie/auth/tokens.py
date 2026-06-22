"""Create and verify JWT access tokens."""

from datetime import datetime, timedelta, timezone

import jwt

from supportgenie.config import settings

SECRET_KEY = settings.jwt_secret_key.get_secret_value()
ALGORITHM = settings.jwt_algorithm
TOKEN_EXPIRE_MINUTES = settings.jwt_expire_minutes


def create_token(username, role):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None