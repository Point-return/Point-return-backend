from math import ceil
from typing import Any, Generic, Type, TypeVar
from datetime import date
import sqlalchemy as sa


from app.core.models import Base
from app.database import async_session_maker
from app.products.models import (
    ParsedProductDealer,
    Product,
    ProductDealer,
    Dealer,
)

Model = TypeVar('Model', bound=Base)


class BaseDAO(Generic[Model]):
    """Интерфейс работы с базой данных."""

    model: Type[Model]

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
            query = sa.select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls) -> Model:
        """Найти все объекты данной модели в базе.

        Returns:
            Все объекты данного типа из базы.
        """
        async with async_session_maker() as session:
            query = sa.select(cls.model)
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
            query = sa.select(cls.model).filter_by(**parameters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data: Any) -> None:
        """Создать объект в базе по данным.

        Args:
            data: данные модели.
        """
        async with async_session_maker() as session:
            query = sa.insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def product_list(
        cls,
        date_from: date,
        date_to: date,
        dealer_id: int,
        page: int,
        limit: int,
    ):
        """Функция для получения всех продуктов."""
        offset = (page - 1) * limit
        async with async_session_maker() as session:
            query = sa.select(ParsedProductDealer.__table__.columns,
                              Product.__table__.columns).\
                select_from(ProductDealer).\
                join(ParsedProductDealer,
                     ProductDealer.key == ParsedProductDealer.product_key,
                     isouter=True).\
                join(Product,
                     ProductDealer.product_id == Product.id,
                     isouter=True).\
                where(
                    sa.and_(ParsedProductDealer.date >= date_from,
                            ParsedProductDealer.date <= date_to)).\
                filter(ProductDealer.dealer_id == dealer_id).\
                offset(offset).\
                limit(limit)
            total = await session.execute(sa.select(ParsedProductDealer.id).\
                select_from(ProductDealer).\
                join(ParsedProductDealer,
                     ProductDealer.key == ParsedProductDealer.product_key,
                     isouter=True).\
                where(
                    sa.and_(ParsedProductDealer.date >= date_from,
                            ParsedProductDealer.date <= date_to)).\
                filter(ProductDealer.dealer_id == dealer_id))
            total_list = ceil(len(total.scalars().all()) / limit)
            result = await session.execute(query)
            response = result.mappings().all() + [
                {
                  "page": page,
                  "size": limit,
                  "total page": total_list,
                }
            ]
            return response

