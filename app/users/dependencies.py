from datetime import datetime
from typing import Awaitable

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.users.dao import UserDAO
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
    token = request.cookies.get('points_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не предоставлен',
        )
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Ошибка распознавания JWT-токена',
        )
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истек',
        )
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не найдеа информация о пользователе в токене',
        )
    user = UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не найден пользователь в базе',
        )
    return user
