from datetime import date
from math import ceil
from typing import Any, Dict

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from app.core.dao import BaseDAO
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
        key_new: str,
        dealer_id_new: int,
        product_id_new: int,
    ) -> ProductDealer:
        """Создать объект связи в базе по данным."""
        try:
            async with async_session_maker() as session:
                query = sa.select(ProductDealer.__table__.columns).filter(
                    ProductDealer.dealer_id == dealer_id_new,
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
                    new_value = (
                        sa.insert(cls.model)
                        .values(
                            id=(max_id + 1),
                            dealer_id=dealer_id_new,
                            key=key_new,
                            product_id=product_id_new,
                        )
                        .returning(
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
