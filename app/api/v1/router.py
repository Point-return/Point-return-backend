from typing import List

from fastapi import APIRouter

from app.api.v1.exceptions import (
    DateError,
    DealerNotFound,
    ParsedDataNotFound,
    ProductDealerNotFound,
    ProductNotFound,
)
from app.api.v1.schemas import (
    DealerSchema,
    MenuSchema,
    MenuValidationSchema,
    ProductSchema,
    ProductValidationSchema,
    RecomendationSchema,
    RecomendationValidationSchema,
    StatisticsSchema,
)
from app.config import logger
from app.core.schemas import EmptySchema
from app.api.v1.date_value import date_val
from app.ds.solution_v_2 import get_solution
from app.products.dao import (
    DealerDAO,
    ParsedProductDealerDAO,
    ProductDAO,
    ProductDealerDAO,
    StatisticsDAO,
)
from app.products.models import ParsedProductDealer
from app.products.utils import generate_product_dealer_key

router_v1 = APIRouter(
    prefix='/v1',
    tags=['Products & Dealers'],
)


@router_v1.get('/dealer/{dealer_id}')
async def dealer_products(
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
    """Get information about all dealer's products.

        Args:
        dealer_id: id of selected dealer.
        size: amount of objects on page.
        page: page number.
        year_from: minimum year of parsing.
        month_from: minimum month of parsing.
        day_from: minimum day of parsing.
        year_to: maximum year of parsing.
        month_to: maximum month of parsing.
        day_to: maximum day of parsing.

    Returns:
        Parsing data according to parameters.
    """
    dealer = await DealerDAO.find_by_id(dealer_id)
    if not dealer:
        logger.error(DealerNotFound.detail)
        raise DealerNotFound
    date_from = date_val(year_from, month_from, day_from)
    date_to = date_val(year_to, month_to, day_to)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
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
    """Get all dealers.

    Returns:
        All dealers data.
    """
    return await DealerDAO.find_all()


@router_v1.get('/recommendations/{dealerprice_id}')
async def get_recommendations(
    dealerprice_id: int,
    limit: int = 10,
) -> List[RecomendationValidationSchema]:
    """Receive a number of recommendations.

    Args:
        dealerprice_id: id of specific parsed data item.
        limit: maximum amount of recommendations.

    Returns:
        List of recommendation products.
    """
    parsed_data: ParsedProductDealer = await ParsedProductDealerDAO.find_by_id(
        dealerprice_id,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    solutions = await get_solution(str(parsed_data.product_name), limit)
    logger.debug(solutions)
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
    """Choose the product from base.

    Args:
        dealerprice_id: specific parsed pada item id.
        product_id: choosed product id.

    Returns:
        Empty responce.
    """
    parsed_data = await ParsedProductDealerDAO.find_by_id(
        dealerprice_id,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    product = await ProductDAO.find_by_id(product_id)
    if not product:
        logger.error(ProductNotFound.detail)
        raise ProductNotFound
    connection = await ProductDealerDAO.find_one_or_none(
        dealer_id=parsed_data.dealer_id,
        product_id=product_id,
    )
    if not parsed_data.product_key:
        await StatisticsDAO.update_success(dealerprice_id)
    if not connection:
        key = await generate_product_dealer_key()
        await ProductDealerDAO.create(
            dealer_id=parsed_data.dealer_id,
            product_id=product_id,
            key=key,
        )
    else:
        if connection.key == parsed_data.product_key:
            return EmptySchema()
        key = await ProductDealerDAO.get_key(
            dealer_id=parsed_data.dealer_id,
            product_id=product_id,
        )
    await ParsedProductDealerDAO.update_key(id=dealerprice_id, key=key)
    return EmptySchema()


@router_v1.patch('/recommendations/{dealerprice_id}/skip')
async def add_skipped(dealerprice_id: int) -> EmptySchema:
    """Mark parsing data as skipped.

    Args:
        dealerprice_id: specific parsed pada item id.

    Returns:
        Empty responce.
    """
    parsed_data = await ParsedProductDealerDAO.find_by_id(
        dealerprice_id,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    if not parsed_data.product_key:
        await StatisticsDAO.update_skip(dealerprice_id)
    return EmptySchema()


@router_v1.get('/statistics')
async def general_static(
    year_from: int = 1900,
    month_from: int = 1,
    day_from: int = 1,
    year_to: int = 2100,
    month_to: int = 1,
    day_to: int = 1,
) -> StatisticsSchema:
    """Get statistics for all dealers.

        Args:
        year_from: minimum year of parsing.
        month_from: minimum month of parsing.
        day_from: minimum day of parsing.
        year_to: maximum year of parsing.
        month_to: maximum month of parsing.
        day_to: maximum day of parsing.

    Returns:
        All statistics information.
    """
    date_from = date_val(year_from, month_from, day_from)
    date_to = date_val(year_to, month_to, day_to)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
    return StatisticsSchema.model_validate(
        await StatisticsDAO.get_general_stat(
            date_from,
            date_to,
        ),
    )


@router_v1.get('/statistics/{dealer_id}')
async def dealer_static(
    dealer_id: int,
    year_from: int = 1900,
    month_from: int = 1,
    day_from: int = 1,
    year_to: int = 2100,
    month_to: int = 1,
    day_to: int = 1,
) -> StatisticsSchema:
    """Get dealer statistics.

        Args:
        dealer_id: id of dealer.
        year_from: minimum year of parsing.
        month_from: minimum month of parsing.
        day_from: minimum day of parsing.
        year_to: maximum year of parsing.
        month_to: maximum month of parsing.
        day_to: maximum day of parsing.

    Returns:
        Statistics corresponding to provided dealer.
    """
    date_from = date_val(year_from, month_from, day_from)
    date_to = date_val(year_to, month_to, day_to)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
    dealer = await DealerDAO.find_by_id(dealer_id)
    if not dealer:
        logger.error(DealerNotFound.detail)
        raise DealerNotFound
    return StatisticsSchema.model_validate(
        await StatisticsDAO.get_dealer_stat(
            dealer_id,
            date_from,
            date_to,
        ),
    )


@router_v1.get('/product/{product_key}')
async def get_product(product_key: int) -> ProductValidationSchema:
    """Get product information by product-dealer connection key.

    Args:
        product_key: product-dealer connection key.

    Returns:
        Product data.
    """
    product_dealer = await ProductDealerDAO.find_one_or_none(key=product_key)
    if not product_dealer:
        logger.error(ProductDealerNotFound.detail)
        raise ProductDealerNotFound
    return ProductValidationSchema(
        **ProductSchema.model_validate(
            await ProductDAO.find_by_id(product_dealer.product_id),
        ).model_dump(),
    )
