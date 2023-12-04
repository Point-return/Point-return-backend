from typing import Dict, Optional

import pytest

from app.config import Roles
from app.users.auth import get_password_hash, verify_password
from app.users.dao import UserDAO
from app.users.models import User


def compare_found_and_provided_users(
    found_user: User,
    provided_user: Dict[str, str],
    is_present: bool,
) -> None:
    """Compare found user data with provided user data.

    Args:
        found_user: user data found in database.
        provided_user: given user_data.
        is_present: expected presence of user in database.
    """
    if is_present:
        assert found_user is not None
        assert found_user.username == provided_user['username']
        assert found_user.email == provided_user['email']
        assert found_user.role == provided_user['role']
        assert verify_password(
            provided_user['password'],
            str(found_user.password),
        )
    else:
        assert not found_user


@pytest.fixture
def user_data(
    request: pytest.FixtureRequest,
    admin: Dict[str, str],
    user: Dict[str, str],
    non_existent_user: Dict[str, str],
) -> Optional[Dict[str, str]]:
    """Iterate email parameters.

    Args:
        request: request to fixture from test.
        admin: admin data fixture.
        user: user data fixture.

    Returns:
        Corresponding email.
    """
    if request.param == 'admin':
        return admin
    elif request.param == 'user':
        return user
    return non_existent_user


@pytest.mark.parametrize(
    'user_id,user_data,is_present',
    [
        (1, 'admin', True),
        (2, 'user', True),
        (100, 'not_existing', False),
    ],
    indirect=['user_data'],
)
async def test_find_user_by_id(
    user_id: int,
    user_data: Dict[str, str],
    is_present: bool,
) -> None:
    """Test finding user by id.

    Args:
        user_id: provided user id.
        user_data: expected user data.
        is_present: expected user presence.
    """
    found_user = await UserDAO.find_by_id(user_id)
    compare_found_and_provided_users(found_user, user_data, is_present)


@pytest.mark.parametrize(
    'user_data,is_present',
    [
        ('admin', True),
        ('user', True),
        ('not_existing', False),
    ],
    indirect=['user_data'],
)
class TestFindUserByParameters:
    """TestClass for finding users by different parameters."""

    async def test_find_user_by_username(
        self,
        user_data: Dict[str, str],
        is_present: bool,
    ) -> None:
        """Test finding user by username.

        Args:
            user_data: provided user data.
            is_present: expected user presence.
        """
        found_user = await UserDAO.find_one_or_none(
            username=user_data['username'],
        )
        compare_found_and_provided_users(found_user, user_data, is_present)

    async def test_find_user_by_email(
        self,
        user_data: Dict[str, str],
        is_present: bool,
    ) -> None:
        """Test finding user by email.

        Args:
            user_data: provided user data.
            is_present: expected user presence.
        """
        found_user = await UserDAO.find_one_or_none(email=user_data['email'])
        compare_found_and_provided_users(found_user, user_data, is_present)

    async def test_find_user_by_username_and_email(
        self,
        user_data: Dict[str, str],
        is_present: bool,
    ) -> None:
        """Test finding user by username and email.

        Args:
            user_data: provided user data.
            is_present: expected user presence.
        """
        found_user = await UserDAO.find_one_or_none(
            username=user_data['username'],
            email=user_data['email'],
        )
        compare_found_and_provided_users(found_user, user_data, is_present)


async def test_find_all_users(
    user: Dict[str, str],
    admin: Dict[str, str],
) -> None:
    """Test finding all users.

    Args:
        user: user data fixture.
        admin: admin data fixture.
    """
    found_users = await UserDAO.find_all()
    compare_found_and_provided_users(found_users[0], admin, True)
    compare_found_and_provided_users(found_users[1], user, True)


class TestCreateDeleteUser:
    """TestClass for creation and deletion of users."""


async def test_creste_ans_delete_user(
    non_existent_user: Dict[str, str],
) -> None:
    """Test user creation and deletion.

    Args:
        non_existent_user: pytest fixture with non-existent user data.
    """
    found_user = await UserDAO.find_one_or_none(
        username=non_existent_user['username'],
        email=non_existent_user['email'],
    )
    compare_found_and_provided_users(found_user, non_existent_user, False)
    await UserDAO.create(
        username=non_existent_user['username'],
        email=non_existent_user['email'],
        password=get_password_hash(non_existent_user['password']),
        role=Roles.user,
    )
    found_user = await UserDAO.find_one_or_none(
        username=non_existent_user['username'],
        email=non_existent_user['email'],
    )
    compare_found_and_provided_users(found_user, non_existent_user, True)
    await UserDAO.delete(
        username=non_existent_user['username'],
        email=non_existent_user['email'],
        role=Roles.user,
    )
    found_user = await UserDAO.find_one_or_none(
        username=non_existent_user['username'],
        email=non_existent_user['email'],
    )
    compare_found_and_provided_users(found_user, non_existent_user, False)
