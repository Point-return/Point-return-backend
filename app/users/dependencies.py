from datetime import datetime
from typing import Awaitable

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import TOKEN_NAME, settings
from app.users.dao import UserDAO
from app.users.exceptions import (
    NoTokenException,
    TokenExpiredException,
    UserInfoNotFoundException,
    WrongTokenException,
    WrongUserInfoException,
)
from app.users.models import User


def get_token(request: Request) -> str:
    """Получение токена из запроса.

    Args:
        request: передаваемый запрос.

    Returns:
        Токен из запроса.

    Raises:
        HTTPException 401: если токен не предоставлен.
    """
    token = request.cookies.get(TOKEN_NAME)
    if not token:
        raise NoTokenException
    return token


def get_current_user(token: str = Depends(get_token)) -> Awaitable[User]:
    """Получение текущего пользователя из запроса.

    Args:
        token: переданный токен.

    Returns:
        Объект пользователя из базы данных.

    Raises:
        HTTPException 401: если токен не декодирован.
        HTTPException 401: если токен истек.
        HTTPException 401: если нет информация о пользователе.
        HTTPException 401: если пользователь не найден в базе.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )

    except JWTError:
        raise WrongTokenException
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserInfoNotFoundException
    user = UserDAO.find_by_id(int(user_id))
    if not user:
        raise WrongUserInfoException
    return user
