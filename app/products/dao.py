from datetime import date
from math import ceil
from typing import Any, Dict
from sqlalchemy.exc import SQLAlchemyError

import sqlalchemy as sa

from app.core.dao import BaseDAO
from app.core.commands import generate_key
from app.database import async_session_maker
from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
)


class ProductDAO(BaseDAO):
    """Интерфейс работы с моделями продуктов."""

    model = Product

    @classmethod
    async def get_ids_names(cls) -> Product:
        """Функция для получения id и name всех продуктов."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.id, cls.model.name)
            result = await session.execute(query)
            return result.mappings().all()


class ProductDealerDAO(BaseDAO):
    """Интерфейс работы с моделями связок продукт-дилер."""

    model = ProductDealer

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


class DealerDAO(BaseDAO):
    """Интерфейс работы с моделями дилеров."""

    model = Dealer


class ParsedProductDealerDAO(BaseDAO):
    """Интерфейс работы с моделями данных парсинга."""

    model = ParsedProductDealer

    @classmethod
    async def product_list(
        cls,
        date_from: date,
        date_to: date,
        dealer_id: int,
        page: int,
        limit: int,
    ) -> Dict[str, Any]:
        """Функция для получения всех данных парсинга."""
        offset = (page - 1) * limit
        async with async_session_maker() as session:
            query = (
                sa.select(cls.model.__table__.columns)
                .select_from(cls.model)
                .where(
                    sa.and_(
                        cls.model.date >= date_from,
                        cls.model.date <= date_to,
                    ),
                )
                .filter(cls.model.dealer_id == dealer_id)
                .offset(offset)
                .limit(limit)
            )
            total = await session.execute(
                sa.select(cls.model.id)
                .where(
                    sa.and_(
                        cls.model.date >= date_from,
                        cls.model.date <= date_to,
                    ),
                )
                .filter(cls.model.dealer_id == dealer_id),
            )
            total_list = ceil(len(total.scalars().all()) / limit)
            result = await session.execute(query)
            items = result.mappings().all()
            response = {
                'items': items,
                'page': page,
                'size': limit,
                'total_page': total_list,
            }
            return response

    @classmethod
    async def get_product_name(cls, id: int) -> str:
        """Функция для получения id и name всех продуктов."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.product_name).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
