from datetime import date
from math import ceil
from typing import Any, Dict, List, Union

import sqlalchemy as sa

from app.core.dao import BaseDAO
from app.database import async_session_maker
from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
    Statistics,
)


class DealerDAO(BaseDAO):
    """Interface for working with dealer models."""

    model = Dealer


class ProductDAO(BaseDAO):
    """Interface for working with product models."""

    model = Product

    @classmethod
    async def get_ids_names(cls) -> List[Dict[str, Any]]:
        """Function to get id and name of all products."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.id, cls.model.name)
            result = await session.execute(query)
            return result.mappings().all()


class ProductDealerDAO(BaseDAO):
    """Interface for working with product-dealer relationship models."""

    model = ProductDealer

    @classmethod
    async def get_min_key(cls) -> int:
        """Get minimum key value."""
        async with async_session_maker() as session:
            query = sa.select(sa.func.min(cls.model.key))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_max_key(cls) -> int:
        """Get maximum key value."""
        async with async_session_maker() as session:
            query = sa.select(sa.func.max(cls.model.key))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_keys(cls) -> List[int]:
        """Get maximum key value."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.key)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_key(
        cls,
        product_id: Union[int, sa.Column[int]],
        dealer_id: Union[int, sa.Column[int]],
    ) -> int:
        """Get key by product_id and dealer_id."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.key).filter_by(
                product_id=product_id,
                dealer_id=dealer_id,
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()


class ParsedProductDealerDAO(BaseDAO):
    """Interface for working with parsing data models."""

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
        """Function to get all parsing data."""
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
        """Function to get id and name of all products."""
        async with async_session_maker() as session:
            query = sa.select(cls.model.product_name).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_key(cls, id: int, key: int) -> None:
        """Update product_key value."""
        async with async_session_maker() as session:
            query = (
                sa.update(cls.model)
                .where(cls.model.id == id)
                .values(product_key=key)
            )
            await session.execute(query)
            await session.commit()


class StatisticsDAO(BaseDAO):
    """Interface of Statictics model."""

    model = Statistics

    @classmethod
    async def update_success(cls, dealerprice_id: int) -> None:
        """Update success value to True."""
        async with async_session_maker() as session:
            query = (
                sa.update(cls.model)
                .where(cls.model.parsed_data_id == dealerprice_id)
                .values(successfull=True)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def cancel_success(cls, dealerprice_id: int) -> None:
        """Update success value to False."""
        async with async_session_maker() as session:
            query = (
                sa.update(cls.model)
                .where(cls.model.parsed_data_id == dealerprice_id)
                .values(successfull=False)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_skip(cls, dealerprice_id: int) -> None:
        """Update product_key value."""
        async with async_session_maker() as session:
            query = (
                sa.update(cls.model)
                .where(cls.model.parsed_data_id == dealerprice_id)
                .values(skipped=True)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_general_stat(cls) -> Dict[str, Any]:
        """Statistics for all dealers."""
        async with async_session_maker() as session:
            query_successfull = (
                sa.select(cls.model.id)
                .join(ParsedProductDealer, cls.model.parsed_data_id
                      == ParsedProductDealer.id, isouter=True)
                .filter(Statistics.successfull == True)
            )
            query_skipped = (
                sa.select(cls.model.id)
                .join(ParsedProductDealer, cls.model.parsed_data_id
                      == ParsedProductDealer.id, isouter=True)
                .filter(Statistics.skipped == True)
            )
            query_successfull = await session.execute(query_successfull)
            query_skipped = await session.execute(query_skipped)
            await session.commit()
            QSuccess = len(query_successfull.mappings().all())
            QSkipped = len(query_skipped.mappings().all())
            try:
                percent = f'{round(QSuccess /(QSuccess + QSkipped) * 100)}%'
            except ZeroDivisionError:
                percent = 'Unknown'
            response = {
                'QuantitySuccessfull': QSuccess,
                'QuantitySkipped': QSkipped,
                'percent': percent,
            }
            return response

    @classmethod
    async def get_dealer_stat(cls, dealer_id: int) -> Dict[str, Any]:
        """Dealer statistics."""
        async with async_session_maker() as session:
            query_successfull = (
                sa.select(cls.model.id)
                .join(ParsedProductDealer, cls.model.parsed_data_id
                      == ParsedProductDealer.id, isouter=True)
                .filter(ParsedProductDealer.dealer_id == dealer_id,
                        Statistics.successfull == True)
            )
            query_skipped = (
                sa.select(cls.model.id)
                .join(ParsedProductDealer, cls.model.parsed_data_id
                      == ParsedProductDealer.id, isouter=True)
                .filter(ParsedProductDealer.dealer_id == dealer_id,
                        Statistics.skipped == True)
            )
            query_successfull = await session.execute(query_successfull)
            query_skipped = await session.execute(query_skipped)
            await session.commit()
            QSuccess = len(query_successfull.mappings().all())
            QSkipped = len(query_skipped.mappings().all())
            try:
                percent = f'{round(QSuccess /(QSuccess + QSkipped) * 100)}%'
            except ZeroDivisionError:
                percent = 'Unknown'
            response = {
                'QuantitySuccessfull': QSuccess,
                'QuantitySkipped': QSkipped,
                'percent': percent,
            }
            return response
        
    @classmethod
    async def cancel_skip(cls, dealerprice_id: int) -> None:
        """Update skipped value to False."""
        async with async_session_maker() as session:
            query = (
                sa.update(cls.model)
                .where(cls.model.parsed_data_id == dealerprice_id)
                .values(skipped=False)
            )
            await session.execute(query)
            await session.commit()
