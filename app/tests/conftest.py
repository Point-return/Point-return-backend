import asyncio
import csv
from typing import Any, AsyncGenerator, Dict, Generator, List

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.core.models import Base
from app.database import async_session_maker, engine
from app.main import app
from app.users.auth import get_password_hash
from app.users.models import User


def open_data(filename: str) -> Dict[str, List[Any]]:
    """Чтение данных пользователя из файла.

    Args:
        filename: имя файла.

    Returns:
        Данные пользователей списком.
    """
    with open(f'app/data/{filename}.csv', 'r') as file:
        data = list(csv.reader(file))
        user_fields = data[0]
        return {'fields': user_fields, 'data': data[1:]}


@pytest.fixture(scope='session')
def admin() -> Dict[str, str]:
    """Данные админа из файла пользователей.

    Returns:
        Словарь с полями и значениями полей админа.
    """
    data = open_data('mock_users')
    return {
        field_name: value
        for field_name, value in zip(data['fields'], data['data'][0])
    }


@pytest.fixture(scope='session')
def user() -> Dict[str, str]:
    """Данные пользователя из файла пользователей.

    Returns:
        Словарь с полями и значениями полей пользователя.
    """
    data = open_data('mock_users')
    return {
        field_name: value
        for field_name, value in zip(data['fields'], data['data'][1])
    }


@pytest.fixture(scope='session', autouse=True)
async def prepate_database(
    admin: Dict[str, Any],
    user: Dict[str, Any],
) -> None:
    """Подготовка базы данных.

    Args:
        admin: fixture с данными админа.
        user: fixture с данными пользователя.
    """
    assert settings.MODE == 'TEST'

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    user = user.copy()
    admin = admin.copy()
    user['password'] = get_password_hash(user['password'])
    admin['password'] = get_password_hash(admin['password'])
    async with async_session_maker() as session:
        add_admin = insert(User).values(**admin)
        add_user = insert(User).values(**user)
        await session.execute(add_admin)
        await session.execute(add_user)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> Generator:
    """Фикстура для создания event loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator:
    """Фикстура для использования асинхронного клиента."""
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
