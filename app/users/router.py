from fastapi import APIRouter, Depends, Response

from app.config import TOKEN_NAME, Roles
from app.core.schemas import EmptySchema
from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.exceptions import (
    InvalidCredentialsException,
    UserEmailAlreadyExistsException,
    UserNameAlreadyExistsException,
)
from app.users.models import User
from app.users.schemas import TokenSchema, UserRegister, UserSafe, UserLogin

router_users = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
)

router_auth = APIRouter(
    prefix='/auth',
    tags=['Авторизация'],
)


@router_auth.post('/register')
async def register_user(user_data: UserRegister) -> EmptySchema:
    """Регистрация пользователя.

    Args:
        user_data: переданные данные пользователя.

    Raises:
        HTTPException 500: если пользователь уже существует.
    """
    existing_user_email = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user_email:
        raise UserEmailAlreadyExistsException
    existing_user_name = await UserDAO.find_one_or_none(
        username=user_data.username,
    )
    if existing_user_name:
        raise UserNameAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.create(
        email=user_data.email,
        password=hashed_password,
        username=user_data.username,
        role=Roles.user,
    )
    return EmptySchema()


@router_auth.post('/login')
async def login_user(
    response: Response,
    user_data: UserLogin,
) -> TokenSchema:
    """Вход пользователя.

    Args:
        response: передаваемый ответ.
        user_data: данные пользователя.

    Raises:
        HTTPException 401: пользователь не зарегистрирован или пароль неверен.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidCredentialsException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(TOKEN_NAME, access_token, httponly=True)
    return TokenSchema(access_token=access_token)


@router_auth.post('/logout')
async def logout_user(response: Response) -> EmptySchema:
    """Вход пользователя.

    Args:
        response: передаваемый ответ.
    """
    response.delete_cookie(TOKEN_NAME)
    return EmptySchema()


@router_users.post('/me')
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> UserSafe:
    """Данные текущего пользователя.

    Args:
        current_user: текущий пользователь.

    Returns:
        Информация о текущем пользователе.
    """
    return UserSafe(
        email=current_user.email,
        username=current_user.username,
    )
