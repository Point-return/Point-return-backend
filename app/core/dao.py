from typing import Any, Generic, Type, TypeVar

from sqlalchemy import delete, insert, select

from app.core.models import Base
from app.database import async_session_maker

Model = TypeVar('Model', bound=Base)


class BaseDAO(Generic[Model]):
    """Database interface."""

    model: Type[Model]

    @classmethod
    async def find_by_id(
        cls,
        model_id: int,
    ) -> Model:
        """Find an object in the database by id.

        Args:
            model_id: id model.

        Returns:
            One object from the database or None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls) -> Model:
        """Find all objects of this model in the database.

        Returns:
            All objects of this type from the database.
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(
        cls,
        **parameters: Any,
    ) -> Model:
        """Find an object in the database using parameters.

        Args:
            parameters: model parameters.

        Returns:
            One object from the database or None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**parameters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data: Any) -> None:
        """Create an object in the database using the data.

        Args:
            data: model data.
        """
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(
        cls,
        **parameters: Any,
    ) -> None:
        """Delete an object in the database using parameters.

        Args:
            parameters: model parameters.
        """
        async with async_session_maker() as session:
            query = delete(cls.model).where(**parameters)
            await session.execute(query)
            await session.commit()
