# mypy: disable-error-code="assignment"
import asyncio
import csv
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Generator, List

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings, Roles
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
from app.products.commands.import_products import import_products
from app.products.commands.import_dealers import import_dealers
from app.products.commands.import_parsed_data import import_parsed_data
from app.products.commands.import_productdealer import import_productdealer
from app.products.dao import ProductDAO, DealerDAO, ProductDealerDAO, ParsedProductDealerDAO
from app.users.auth import get_password_hash
from app.users.models import User
from app.users.dao import UserDAO
from app.users.commands.import_users import import_users


@pytest.fixture(scope='session')
async def users() -> Dict[str, User]:
    """Provide test data of admin from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Admin data from file.
    """
    assert settings.MODE == 'TEST'
    import_users()
    return {'admin': await UserDAO.find_one_or_none(role=Roles.admin),
            'user': await UserDAO.find_one_or_none(role=Roles.user),
    }

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
async def products() -> List[Product]:
    """Provide test data of products from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Products data from file.
    """
    assert settings.MODE == 'TEST'
    import_products()
    return await ProductDAO.find_all()


@pytest.fixture(scope='session')
async def dealers() -> List[Dealer]:
    """Provide test data of dealers from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Dealers data from file.
    """
    assert settings.MODE == 'TEST'
    import_dealers()
    return await DealerDAO.find_all()


@pytest.fixture(scope='session')
async def product_dealer() -> List[ProductDealer]:
    """Provide test data of product-dealer keys from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Product-dealer keys data from file.
    """
    assert settings.MODE == 'TEST'
    import_productdealer()
    return await ProductDealerDAO.find_all()


@pytest.fixture(scope='session')
async def parsed_data() -> List[ParsedProductDealer]:
    """Provide test parsed data from file.

    Args:
        filenames: names of files with test data.

    Returns:
        Parsed data from file.
    """
    assert settings.MODE == 'TEST'
    import_parsed_data()
    return await ParsedProductDealerDAO.find_all()


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
