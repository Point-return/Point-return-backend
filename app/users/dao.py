from typing import List
from app.core.dao import BaseDAO
from app.users.models import User

from sqlalchemy import select
from app.database import async_session_maker


class UserDAO(BaseDAO):
    """Interface for working with user models."""

    model = User

    @classmethod
    async def get_names(cls) -> List[str]:
        """Find all usernames from the database.

        Returns:
            All usernames from the database.
        """
        async with async_session_maker() as session:
            query = select(cls.model.username)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def get_emails(cls) -> List[str]:
        """Find all emails from the database.

        Returns:
            All emails from the database.
        """
        async with async_session_maker() as session:
            query = select(cls.model.email)
            result = await session.execute(query)
            return result.scalars().all()
