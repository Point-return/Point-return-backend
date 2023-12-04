from typing import Any, Generic, TypeVar

from sqlalchemy import delete, insert, select

from app.core.models import Base
from app.database import async_session_maker

Model = TypeVar('Model', bound=Base)


class BaseDAO(Generic[Model]):
    """Интерфейс работы с базой данных."""

    model = Model  # type: ignore[misc]

    @classmethod
    async def find_by_id(
        cls,
        model_id: int,
    ) -> Model:
        """Найти объект в базе по id.

        Args:
            model_id: id модели.

        Returns:
            Один объект из базы данных или None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls) -> Model:
        """Найти все объекты данной модели в базе.

        Returns:
            Все объекты данного типа из базы.
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
        """Найти объект в базе по параметрам.

        Args:
            parameters: параметры модели.

        Returns:
            Один объект из базы данных или None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**parameters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data: Any) -> None:
        """Создать объект в базе по данным.

        Args:
            data: данные модели.
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
        """Удалить объект в базе по параметрам.

        Args:
            parameters: параметры модели.
        """
        async with async_session_maker() as session:
            model_parameters = [
                getattr(cls.model, key) == value
                for key, value in parameters.items()
            ]
            query = delete(cls.model).where(*model_parameters)
            await session.execute(query)
            await session.commit()
