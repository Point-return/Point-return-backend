from typing import List

from fastapi import APIRouter, Depends

from app.products.dao import ProductDAO
from app.products.schemas import ProductSchema
from app.users.dependencies import get_current_user
from app.users.models import User

router_products = APIRouter(
    prefix='/products',
    tags=['Продукты & Дилеры'],
)


@router_products.get('/')
async def get_products(
    user: User = Depends(get_current_user),
) -> List[ProductSchema]:
    """Функция для получения всех продуктов.

    Args:
        user: пользователь, определённый по JWT-токену.

    Returns:
        Все продукты из базы данных.
    """
    return await ProductDAO.find_all()