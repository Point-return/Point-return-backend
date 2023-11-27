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
    """Хэширование пароля.

    Args:
        passworg: пароль.

    Returns:
        Хэшированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля.

    Args:
        plain_password: введённый пароль.
        hashed_password: хэшированный пароль.

    Returns:
        Соответствие паролей.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Создание токена авторизации.

    Args:
        data: данные для создания токена.

    Returns:
        Токен авторизации.
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
    """Авторизация пользователя.

    Args:
        email: email пользователя.
        password: пароль пользователя.

    Returns:
        Объект пользователя из базы данных или None.
    """
    user = await UserDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.password):
        return user
    return None
