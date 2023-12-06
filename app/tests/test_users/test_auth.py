from typing import Dict, Optional

import pytest
from fastapi import status
from httpx import AsyncClient
from app.users.models import User


@pytest.mark.parametrize(
    'username,email,password,status_code',
    [
        (
            'non_existing_user_1',
            'non_existing_user_1@mail.ru',
            'test_password1',
            status.HTTP_200_OK,
        ),
        (
            'non_existing_user_1',
            'non_existing_user_1@mail.ru',
            'test_password2',
            status.HTTP_409_CONFLICT,
        ),
        (
            'non_existing_user_2',
            'non_existing_user_2@mail.ru',
            'test_password1',
            status.HTTP_200_OK,
        ),
        ('some', 'not_valid', 'some', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_registed_user(
    username: str,
    email: str,
    password: str,
    status_code: int,
    async_client: AsyncClient,
) -> None:
    """Test user registration.

    Args:
        username: pytest parameter with usernames.
        email: pytest parameter with emails.
        password: pytest parameter with passwords.
        status_code: expected status codes.
        async_client: asynchronous client fixture.
    """
    responce = await async_client.post(
        '/auth/register',
        json={
            'username': username,
            'email': email,
            'password': password,
        },
    )
    assert responce.status_code == status_code


@pytest.fixture
def email(
    request: pytest.FixtureRequest,
    users: Dict[str, User],
) -> Optional[str]:
    """Iterate email parameters.

    Args:
        request: request to fixture from test.
        admin: admin data fixture.
        user: user data fixture.

    Returns:
        Corresponding email.
    """
    if request.param == 'admin':
        return users['admin'].email
    elif request.param == 'user':
        return users['user'].email
    elif request.param == 'not_existing':
        return 'not_existing@mail.ru'
    elif request.param == 'not_valid':
        return 'not_valid'
    return None


@pytest.fixture
def password(
    request: pytest.FixtureRequest,
    users: Dict[str, User],
) -> Optional[str]:
    """Iterate password parameters.

    Args:
        request: request to fixture from test.
        admin: admin data fixture.
        user: user data fixture.

    Returns:
        Corresponding password.
    """
    if request.param == 'admin':
        return users['admin'].password
    elif request.param == 'user':
        return users['user'].password
    elif request.param == 'some':
        return 'some_password'
    return None


@pytest.mark.parametrize(
    'email,password,status_code',
    [
        ('admin', 'admin', status.HTTP_200_OK),
        ('user', 'user', status.HTTP_200_OK),
        ('not_existing', 'some', status.HTTP_403_FORBIDDEN),
        ('not_valid', 'some', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
    indirect=['email', 'password'],
)
async def test_login_user(
    email: str,
    password: str,
    status_code: int,
    async_client: AsyncClient,
) -> None:
    """Тестирование логина пользователей.

    Args:
        email: параметр pytest с почтами пользователей.
        password: параметр pytest с паролями пользователей.
        status_code: параметр pytest со статус-кодом ответа.
        async_client: асинхронный клиент.
    """
    responce = await async_client.post(
        '/auth/login',
        json={
            'email': email,
            'password': password,
        },
    )
    assert responce.status_code == status_code
