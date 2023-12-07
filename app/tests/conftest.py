# mypy: disable-error-code="assignment"
import asyncio
import csv
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Generator, List

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.core.models import Base
from app.core.utils import (
    convert_string_to_float,
    convert_to_float_and_truncate,
)
from app.database import async_session_maker, engine
from app.main import app
from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
    Statistics,
)
from app.users.auth import get_password_hash
from app.users.models import User


def open_data(filename: str) -> List[Dict[str, str]]:
    """Read test data from tile.

    Args:
        filename: name of file.

    Returns:
        Data from file.
    """
    with open(f'app/data/{filename}.csv', 'r', encoding='utf-8-sig') as file:
        data = list(csv.reader(file, delimiter=';'))
        fields = data[0]
        return [
            {field_name: value for field_name, value in zip(fields, item)}
            for item in data[1:]
        ]


@pytest.fixture(scope='session')
def filenames() -> Dict[str, str]:
    """Provide names of files with test data.

    Returns:
        Names of files with test data.
    """
    return {
        'users': 'test_users',
        'products': 'test_products',
        'dealers': 'test_dealers',
        'product-dealer': 'test_productdealer',
        'parsed data': 'test_dealerprice',
    }


@pytest.fixture(scope='session')
def admin(filenames: Dict[str, str]) -> Dict[str, str]:
    """Provide test data of admin from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Admin data from file.
    """
    return open_data(filenames['users'])[0]


@pytest.fixture(scope='session')
def user(filenames: Dict[str, str]) -> Dict[str, str]:
    """Provide test data of user from file.

    Args:
        filenames: names of files with test data.

    Returns:
        User data from file.
    """
    return open_data(filenames['users'])[1]


@pytest.fixture(scope='session')
def non_existent_user() -> Dict[str, str]:
    """Provide test data of non-existent user.

    Returns:
        Non-existent user data.
    """
    return {
        'email': 'non-existent@mail.ru',
        'username': 'non-existent',
        'password': 'some',
        'role': 'user',
    }


@pytest.fixture(scope='session')
def products(filenames: Dict[str, str]) -> List[Dict[str, Any]]:
    """Provide test data of products from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Products data from file.
    """
    data = open_data(filenames['products'])
    for item in data:
        item['id'] = int(item['id'])
        item['ean_13'] = convert_to_float_and_truncate(item['ean_13'])
        item['cost'] = float(item['cost'])
        item['recommended_price'] = float(item['recommended_price'])
        item['category_id'] = convert_to_float_and_truncate(
            item['category_id'],
        )
        item['ozon_article'] = convert_to_float_and_truncate(
            item['ozon_article'],
        )
        item['wb_article'] = convert_to_float_and_truncate(item['wb_article'])
    return data


@pytest.fixture(scope='session')
def dealers(filenames: Dict[str, str]) -> List[Dict[str, Any]]:
    """Provide test data of dealers from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Dealers data from file.
    """
    data = open_data(filenames['dealers'])
    for item in data:
        item['id'] = int(item['id'])
    return data


@pytest.fixture(scope='session')
def product_dealer(filenames: Dict[str, str]) -> List[Dict[str, Any]]:
    """Provide test data of product-dealer keys from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Product-dealer keys data from file.
    """
    data = open_data(filenames['product-dealer'])
    for item in data:
        item['dealer_id'] = int(item['dealer_id'])
        item['product_id'] = int(item['product_id'])
        item['key'] = int(item['key'])
    return data


@pytest.fixture(scope='session')
def parsed_data(filenames: Dict[str, str]) -> List[Dict[str, Any]]:
    """Provide test parsed data from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Parsed data from file.
    """
    data = open_data(filenames['parsed data'])
    for item in data:
        item['dealer_id'] = int(item['dealer_id'])
        item['id'] = int(item['id'])
        item['price'] = convert_string_to_float(item['price'])
        item['date'] = datetime.strptime(item['date'], '%Y-%m-%d').date()
    return data


@pytest.fixture(scope='session', autouse=True)
async def prepate_database(
    admin: Dict[str, Any],
    user: Dict[str, Any],
    products: List[Dict[str, Any]],
    dealers: List[Dict[str, Any]],
    product_dealer: List[Dict[str, Any]],
    parsed_data: List[Dict[str, Any]],
) -> None:
    """Prepare database.

    Args:
        admin: fixture with admin data.
        user: fixture with user data.
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
        add_products = insert(Product).values(products)
        add_dealers = insert(Dealer).values(dealers)
        add_product_dealer = insert(ProductDealer).values(product_dealer)
        add_parsed_data = insert(ParsedProductDealer).values(parsed_data)
        add_statistics = insert(Statistics).values(
            [
                {'parsed_data_id': parsed_data_item['id']}
                for parsed_data_item in parsed_data
            ],
        )
        await session.execute(add_admin)
        await session.execute(add_user)
        await session.execute(add_products)
        await session.execute(add_dealers)
        await session.execute(add_product_dealer)
        await session.execute(add_parsed_data)
        await session.execute(add_statistics)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> Generator:
    """Create event loop.

    Args:
        reauest: request for fixture.

    Returns:
        Created loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator:
    """Create asynchronous test client."""
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
