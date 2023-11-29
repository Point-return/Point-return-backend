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
        limit=10,
        date_from=datetime(1900, 1, 1),
        date_to=datetime(2100, 1, 1),
):
    """Функция для получения всех продуктов.

    Args:
        user: пользователь, определённый по JWT-токену.

    Returns:
        Все продукты из базы данных.
    """
    return await ProductDAO.main_list(
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
