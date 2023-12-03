from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends

from app.products.dao import ProductDAO, DealerDAO, ProductDealerDAO
from app.products.schemas import ProductSchema, SNewProductDealerKey
from app.users.dependencies import get_current_user
from app.users.models import User

from app.solution import get_solution, get_suitable_products

router_products = APIRouter(
    prefix='',
    tags=['Продукты & Дилеры'],
)


@router_products.get('/dealer/{dealer_id}')
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
                          ):
    """Функция для получения информации всех продуктов дилера."""
    date_from = datetime(int(year_from), int(month_from), int(day_from))
    date_to = datetime(int(year_to), int(month_to), int(day_to))
    return await ProductDAO.product_list(
        dealer_id=dealer_id,
        limit=size,
        page=page,
        date_from=date_from,
        date_to=date_to,
        )


@router_products.get('/dealers')
async def get_dealers():
    """Функция для получения всех дилеров."""
    return await DealerDAO.find_all()

@router_products.get('/productdealer/{id}')
async def product_key(id: int):
    """Функция для получения информации о продукте дилера."""

    return await ProductDealerDAO.find_by_id(id)

@router_products.post('/productdealer')
async def add_product_key(
        productdealer: SNewProductDealerKey):
    """Функция для получения информации всех продуктов дилера."""

    return await ProductDealerDAO.add(
        productdealer.key,
        productdealer.dealer_id,
        productdealer.product_id,
        )
