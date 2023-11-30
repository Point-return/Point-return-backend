from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends

from app.products.dao import ProductDAO, DealerDAO
from app.products.schemas import ProductSchema
from app.users.dependencies import get_current_user
from app.users.models import User

router_products = APIRouter(
    prefix='',
    tags=['Продукты & Дилеры'],
)


@router_products.get('/products')
async def get_products(
        limit: int = 10,
        year_from: int = 1900,
        month_from: int = 1,
        day_from: int = 1,
        year_to: int = 2100,
        month_to: int = 1,
        day_to: int = 1,
):
    """Функция для получения всех продуктов.

    Args:
        

    Returns:
        Все продукты из базы данных.
    """
    date_from = datetime(int(year_from), int(month_from), int(day_from))
    date_to = datetime(int(year_to), int(month_to), int(day_to))
    return await ProductDAO.main_list(
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )


@router_products.get('/dialer/{dialer_id}')
async def dialer_products(
        dialer_id: int,
        limit: int = 10,
        year_from: int = 1900,
        month_from: int = 1,
        day_from: int = 1,
        year_to: int = 2100,
        month_to: int = 1,
        day_to: int = 1,
                        ):
    """Функция для получения информации всех продуктов дилера."""
    date_from = datetime(int(year_from), int(month_from), int(day_from))
    date_to = datetime(int(year_to), int(month_to), int(day_to))
    return await ProductDAO.product_list(
        dialer_id=dialer_id,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
        )


@router_products.get('/dialers')
async def get_dialers():
    """Функция для получения всех дилеров."""
    return await DealerDAO.find_all()
