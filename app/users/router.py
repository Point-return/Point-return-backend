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
from app.users.schemas import TokenSchema, UserLogin, UserRegister, UserSafe

router_users = APIRouter(
    prefix='/users',
    tags=['Users'],
)

router_auth = APIRouter(
    prefix='/auth',
    tags=['Authorization'],
)


@router_auth.post('/register')
async def register_user(user_data: UserRegister) -> EmptySchema:
    """User registration.

    Args:
        user_data: transferred user data.

    Raises:
        HTTPException 500: if the user already exists.
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
    """User Login.

    Args:
        response: transmitted response.
        user_data: user data.

    Raises:
        HTTPException 401: the user is not registered
        or the password is incorrect.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidCredentialsException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(TOKEN_NAME, access_token, httponly=True)
    return TokenSchema(accessToken=access_token)


@router_auth.post('/logout')
async def logout_user(response: Response) -> EmptySchema:
    """User logout.

    Args:
        response: transmitted response.
    """
    response.delete_cookie(TOKEN_NAME)
    return EmptySchema()


@router_users.get('/me')
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> UserSafe:
    """Get current user info.

    Args:
        current_user: current user.

    Returns:
        Current user information.
    """
    return await current_user  # type: ignore[misc]
