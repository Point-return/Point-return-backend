from typing import Dict

from fastapi import APIRouter, HTTPException, Response, status

from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UserDAO
from app.users.schemas import UserAuth

router_user = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи'],
)


@router_user.post('/register')
async def register_user(user_data: UserAuth) -> None:
    """Регистрация пользователя.

    Args:
        Переданные данные пользователей.

    Raises:
        HTTPException 500: если пользователь уже существует.
    """
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Пользователь уже существует',
        )
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.create(
        email=user_data.email,
        password=hashed_password,
        username=user_data.username,
    )


@router_user.post('/login')
async def login_user(
    response: Response,
    user_data: UserAuth,
) -> Dict[str, str]:
    """Вход пользователя.

    Args:
        response: переданный запрос.
        user_data: данные пользователя.

    Raises:
        HTTPException 401: пользователь не зарегистрирован или пароль неверен.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не зарегистрирован или неверный пароль',
        )
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('points_access_token', access_token, httponly=True)
    return {'access_token': access_token}
