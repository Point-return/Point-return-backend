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
    """Getting a token from a request.

    Args:
        request: transmitted request.

    Returns:
        Token from request.

    Raises:
        HTTPException 401: if token is not provided.
    """
    token = request.cookies.get(TOKEN_NAME)
    if not token:
        raise NoTokenException
    return token


def get_current_user(token: str = Depends(get_token)) -> Awaitable[User]:
    """Getting the current user from a request.

    Args:
        token: transferred token.

    Returns:
        User object from database.

    Raises:
        HTTPException 401: if the token is not decoded.
        HTTPException 401: if the token has expired.
        HTTPException 401: if there is no user information.
        HTTPException 401: if the user is not found in the database.
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
