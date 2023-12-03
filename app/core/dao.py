from math import ceil
from typing import Any, Generic, Type, TypeVar
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
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
            query = sa.select(ParsedProductDealer.__table__.columns).\
                select_from(ParsedProductDealer).\
                where(
                    sa.and_(ParsedProductDealer.date >= date_from,
                            ParsedProductDealer.date <= date_to)).\
                filter(ParsedProductDealer.dealer_id == dealer_id).\
                offset(offset).\
                limit(limit)
            total = await session.execute(sa.select(ParsedProductDealer.id).\
                where(
                    sa.and_(ParsedProductDealer.date >= date_from,
                            ParsedProductDealer.date <= date_to)).\
                filter(ParsedProductDealer.dealer_id == dealer_id))
            total_list = ceil(len(total.scalars().all()) / limit)
            result = await session.execute(query)
            items = result.mappings().all()
            response = {
                  "items": items,
                  "page": page,
                  "size": limit,
                  "total_page": total_list,
                        }
            return response

    @classmethod
    async def add(
        cls,
        key_new: str,
        dealer_id_new: int,
        product_id_new: int,
    ):
        """Создать объект в базе по данным.

        Args:
            data: данные модели.
        """
        try:
            async with async_session_maker() as session:
                query = sa.select(ProductDealer.__table__.columns).\
                    filter(ProductDealer.dealer_id == dealer_id_new,
                           ProductDealer.key == key_new,
                           ProductDealer.product_id == product_id_new,
                           )
                result = await session.execute(query)
                items = result.mappings().all()
                if items:
                    return {
                        'msg': 'Запись уже существует',
                        'items': items,
                    }
                else:
                    number = sa.func.max(ProductDealer.id)
                    result = await session.execute(number)
                    max_id = result.scalar()
                    new_value = (sa.insert(cls.model).values(
                        id=(max_id + 1),
                        dealer_id=dealer_id_new,
                        key=key_new,
                        product_id=product_id_new,
                    ).returning(
                        ProductDealer.id,
                        ProductDealer.key,
                        ProductDealer.product_id,
                        ProductDealer.dealer_id,
                    )
                    )
                    new_record = await session.execute(new_value)
                    await session.commit()
                    return {
                        'msg': 'Запись добавлена',
                        'items': new_record.mappings().all(),
                    }
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = 'Ошибка связи с БД'
            elif isinstance(e, Exception):
                msg = 'Unknown Exc: Cannot add booking'
            return {
                'msg': msg,
            }
