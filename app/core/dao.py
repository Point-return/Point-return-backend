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
        dealer_id_new: int,
        product_id_new: int,
        product_name: str,
        product_url: str,
        date: date,
    ):
        """Создать объект связи в базе по данным."""
        try:
            async with async_session_maker() as session:
                query = sa.select(ParsedProductDealer.__table__.columns,
                                  ProductDealer.__table__.columns).\
                    join(ProductDealer, ParsedProductDealer.product_key
                         == ProductDealer.key, isouter=True).\
                    filter(ParsedProductDealer.dealer_id == dealer_id_new,
                           ParsedProductDealer.product_name == product_name,
                           ParsedProductDealer.product_url == product_url,
                           ParsedProductDealer.date == date,
                           ProductDealer.dealer_id == dealer_id_new,
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
                    check = sa.select(ParsedProductDealer.__table__.columns).\
                        filter(ParsedProductDealer.dealer_id == dealer_id_new,
                               ParsedProductDealer.product_name
                               == product_name,
                               ParsedProductDealer.product_url == product_url,
                               ParsedProductDealer.date == date,
                               )
                    result = await session.execute(check)
                    items = result.mappings().all()
                    if not items:
                        return {
                            'msg': 'Записи о продукте нет',
                        }
                    else:
                        flag = 0
                        while flag == 0:
                            gen_key = generate_key.create_code()
                            key_check = sa.select(ProductDealer.key).\
                                filter(ProductDealer.key == gen_key)
                            result = await session.execute(key_check)
                            key_check = result.scalar()
                            if key_check != gen_key:
                                flag = 1
                        number = sa.func.max(ProductDealer.id)
                        result = await session.execute(number)
                        max_id = result.scalar()
                        new_ProductDealer = (sa.insert(cls.model).values(
                            id=(max_id + 1),
                            dealer_id=dealer_id_new,
                            key=gen_key,
                            product_id=product_id_new,
                        ).returning(
                            ProductDealer.id,
                            ProductDealer.key,
                            ProductDealer.product_id,
                            ProductDealer.dealer_id,
                        )
                        )
                        new_ProductDealer = await session.execute(
                            new_ProductDealer)
                        new_ParsedProduct = sa.update(ParsedProductDealer,
                                                      ).values(
                            product_key=gen_key,
                        ).where(
                            ParsedProductDealer.product_name == product_name,
                            ParsedProductDealer.date == date,
                            ParsedProductDealer.product_url == product_url,
                            ParsedProductDealer.dealer_id == dealer_id_new,
                        ).returning(
                            ParsedProductDealer.id,
                            ParsedProductDealer.product_key,
                            ParsedProductDealer.product_name,
                            ParsedProductDealer.dealer_id,
                        )
                        new_ParsedProduct = await session.execute(
                            new_ParsedProduct)
                        await session.commit()
                        return {
                            'msg': 'Запись добавлена',
                            'newParsedProduct':
                                new_ParsedProduct.mappings().all(),
                            'newProductDealer':
                                new_ProductDealer.mappings().all(),
                        }
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = 'Ошибка связи с БД'
            elif isinstance(e, Exception):
                msg = 'Ошибка'
            return {
                'msg': msg,
            }
