from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends

from app.products.dao import ProductDAO
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


@router_products.get('/products/{product_id}')
async def get_product(product_id: int):
    """Функция для получения информации о продукте.

    Args:
        product_id 

    Returns:
        Информация о продукте из базы данных.
    """
    return await ProductDAO.find_by_id(product_id)
