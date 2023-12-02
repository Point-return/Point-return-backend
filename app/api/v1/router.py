from datetime import datetime
from typing import List

from fastapi import APIRouter

from app.api.v1.exceptions import ParsedDataNotFound
from app.api.v1.schemas import (
    DealerSchema,
    MenuSchema,
    MenuValidationSchema,
    RecomendationSchema,
    RecomendationValidationSchema,
)
from app.ds.solution import get_solution
from app.products.dao import DealerDAO, ParsedProductDealerDAO

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
        **MenuSchema.parse_obj(
            await ParsedProductDealerDAO.product_list(
                dealer_id=dealer_id,
                limit=size,
                page=page,
                date_from=date_from,
                date_to=date_to,
            ),
        ).dict(),
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
    dealer_product_name = await ParsedProductDealerDAO.get_product_name(
        dealerprice_id,
    )
    if not dealer_product_name:
        raise ParsedDataNotFound
    solutions = await get_solution(dealer_product_name)
    return [
        RecomendationValidationSchema(
            **RecomendationSchema.parse_obj(solution).dict(),
        )
        for solution in solutions
    ]
