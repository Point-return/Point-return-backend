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
