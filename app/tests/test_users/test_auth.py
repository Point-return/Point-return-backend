import pytest
from fastapi import status
from httpx import AsyncClient


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
    """Тестирование регистрации пользователей.

    Args:
        username: параметр pytest с именами пользователей.
        email: параметр pytest с почтами пользователей.
        password: параметр pytest с паролями пользователей.
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
