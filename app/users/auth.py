from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Password Hashing.

    Args:
        password: password.

    Returns:
        Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Password verification.

    Args:
        plain_password: entered password.
        hashed_password: hashed password.

    Returns:
        Password matching.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Creating an Authorization Token.

    Args:
        data: data for creating a token.

    Returns:
        Authorization token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> Optional[User]:
    """User authorization.

    Args:
        email: user email.
        password: user password.

    Returns:
        User object from database or None.
    """
    user = await UserDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.password):
        return user
    return None


async def authenticate_user_by_username(
    username: str,
    password: str,
) -> Optional[User]:
    """User authorization by name.

    Args:
        username: Username.
        password: user password.

    Returns:
        User object from database or None.
    """
    user = await UserDAO.find_one_or_none(username=username)
    if user and verify_password(password, user.password):
        return user
    return None
