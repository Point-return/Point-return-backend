from datetime import datetime
from typing import List

from fastapi import APIRouter

from app.api.v1.exceptions import ConnectionAlreadyExists, ParsedDataNotFound
from app.api.v1.schemas import (
    DealerSchema,
    MenuSchema,
    MenuValidationSchema,
    RecomendationSchema,
    RecomendationValidationSchema,
)
from app.core.schemas import EmptySchema
from app.ds.solution_v_2 import get_solution
from app.products.dao import (
    DealerDAO,
    ParsedProductDealerDAO,
    ProductDealerDAO,
    StatisticsDAO,
)
from app.products.models import ParsedProductDealer
from app.products.utils import generate_product_dealer_key

router_v1 = APIRouter(
    prefix='/v1',
    tags=['Продукты & Дилеры'],
)


@router_v1.get('/dealer/{dealer_id}')
async def dialer_products(
    dealer_id: int,
    size: int = 50,
    page: int = 1,
    year_from: int = 1900,
    month_from: int = 1,
    day_from: int = 1,
    year_to: int = 2100,
    month_to: int = 1,
    day_to: int = 1,
) -> MenuValidationSchema:
    """Функция для получения информации всех продуктов дилера."""
    date_from = datetime(int(year_from), int(month_from), int(day_from))
    date_to = datetime(int(year_to), int(month_to), int(day_to))
    return MenuValidationSchema(
        **MenuSchema.model_validate(
            await ParsedProductDealerDAO.product_list(
                dealer_id=dealer_id,
                limit=size,
                page=page,
                date_from=date_from,
                date_to=date_to,
            ),
        ).model_dump(),
    )


@router_v1.get('/dealers')
async def get_dealers() -> List[DealerSchema]:
    """Функция для получения всех дилеров."""
    return await DealerDAO.find_all()


@router_v1.get('/recommendations/{dealerprice_id}')
async def get_recommendations(
    dealerprice_id: int,
    limit: int = 10,
) -> List[RecomendationValidationSchema]:
    """Функция для получения рекомендаций."""
    parsed_data: ParsedProductDealer = await ParsedProductDealerDAO.find_by_id(
        dealerprice_id,
    )
    if not parsed_data:
        raise ParsedDataNotFound
    if parsed_data.product_key:
        raise ConnectionAlreadyExists
    solutions = await get_solution(str(parsed_data.product_name), limit)
    return [
        RecomendationValidationSchema(
            **RecomendationSchema.model_validate(solution).model_dump(),
        )
        for solution in solutions
    ]


@router_v1.patch('/recommendations/{dealerprice_id}/choose')
async def add_product_key(
    dealerprice_id: int,
    product_id: int,
) -> EmptySchema:
    """Choosing the product from base."""
    parsed_data: ParsedProductDealer = await ParsedProductDealerDAO.find_by_id(
        dealerprice_id,
    )
    if not parsed_data:
        raise ParsedDataNotFound
    if parsed_data.product_key:
        raise ConnectionAlreadyExists
    connection = await ProductDealerDAO.find_one_or_none(
        dealer_id=parsed_data.dealer_id,
        product_id=product_id,
    )
    if not connection:
        key = await generate_product_dealer_key()
        await ProductDealerDAO.create(
            dealer_id=parsed_data.dealer_id,
            product_id=product_id,
            key=key,
        )
    else:
        key = await ProductDealerDAO.get_key(
            dealer_id=parsed_data.dealer_id,
            product_id=product_id,
        )
    await ParsedProductDealerDAO.update_key(id=dealerprice_id, key=key)
    await StatisticsDAO.update_success(dealerprice_id)
    return EmptySchema()


@router_v1.patch('/recommendations/{dealerprice_id}/skip')
async def add_skipped(dealerprice_id: int) -> EmptySchema:
    """Add skipped."""
    await StatisticsDAO.update_skip(dealerprice_id)
    return EmptySchema()
