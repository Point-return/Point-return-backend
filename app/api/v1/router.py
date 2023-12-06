from typing import List

from fastapi import APIRouter, Depends

from app.api.v1.date_value import date_val
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
from app.users.dependencies import get_current_user
from app.users.exceptions import InvalidCredentialsException
from app.users.models import User

router_v1 = APIRouter(
    prefix='/v1',
    tags=['Products & Dealers'],
)


@router_v1.get('/dealer/{dealerId}')
async def dealer_products(
    dealerId: int,
    size: int = 50,
    page: int = 1,
    yearFrom: int = 1900,
    monthFrom: int = 1,
    dayFrom: int = 1,
    yearTo: int = 2100,
    monthTo: int = 1,
    dayTo: int = 1,
) -> MenuValidationSchema:
    """Get information about all dealer's products.

        Args:
        dealerId: id of selected dealer.
        size: amount of objects on page.
        page: page number.
        yearFrom: minimum year of parsing.
        monthFrom: minimum month of parsing.
        dayFrom: minimum day of parsing.
        yearTo: maximum year of parsing.
        monthTo: maximum month of parsing.
        dayTo: maximum day of parsing.

    Returns:
        Parsing data according to parameters.
    """
    dealer = await DealerDAO.find_by_id(dealerId)
    if not dealer:
        logger.error(DealerNotFound.detail)
        raise DealerNotFound
    date_from = date_val(yearFrom, monthFrom, dayFrom)
    date_to = date_val(yearTo, monthTo, dayTo)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
    return MenuValidationSchema(
        **MenuSchema.model_validate(
            await ParsedProductDealerDAO.product_list(
                dealer_id=dealerId,
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


@router_v1.get('/recommendations/{dealerpriceId}')
async def get_recommendations(
    dealerpriceId: int,
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
        dealerpriceId,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    solutions = await get_solution(str(parsed_data.product_name), limit)
    return [
        RecomendationValidationSchema(
            **RecomendationSchema.model_validate(solution).model_dump(),
        )
        for solution in solutions
    ]


@router_v1.patch('/recommendations/{dealerpriceId}/choose')
async def add_product_key(
    dealerpriceId: int,
    productId: int,
) -> EmptySchema:
    """Choose the product from base.

    Args:
        dealerpriceId: specific parsed pada item id.
        productId: choosed product id.

    Returns:
        Empty responce.
    """
    parsed_data = await ParsedProductDealerDAO.find_by_id(
        dealerpriceId,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    product = await ProductDAO.find_by_id(productId)
    if not product:
        logger.error(ProductNotFound.detail)
        raise ProductNotFound
    connection = await ProductDealerDAO.find_one_or_none(
        dealer_id=parsed_data.dealer_id,
        product_id=productId,
    )
    if not parsed_data.product_key:
        await StatisticsDAO.update_success(dealerpriceId)
    if not connection:
        key = await generate_product_dealer_key()
        await ProductDealerDAO.create(
            dealer_id=parsed_data.dealer_id,
            product_id=productId,
            key=key,
        )
    else:
        if connection.key == parsed_data.product_key:
            return EmptySchema()
        key = await ProductDealerDAO.get_key(
            dealer_id=parsed_data.dealer_id,
            product_id=productId,
        )
    await ParsedProductDealerDAO.update_key(id=dealerpriceId, key=key)
    return EmptySchema()


@router_v1.patch('/recommendations/{dealerpriceId}/skip')
async def add_skipped(dealerpriceId: int) -> EmptySchema:
    """Mark parsing data as skipped.

    Args:
        dealerpriceId: specific parsed pada item id.

    Returns:
        Empty responce.
    """
    parsed_data = await ParsedProductDealerDAO.find_by_id(
        dealerpriceId,
    )
    if not parsed_data:
        logger.error(ParsedDataNotFound.detail)
        raise ParsedDataNotFound
    if not parsed_data.product_key:
        await StatisticsDAO.update_skip(dealerpriceId)
    return EmptySchema()


@router_v1.get('/statistics')
async def general_static(
    yearFrom: int = 1900,
    monthFrom: int = 1,
    dayFrom: int = 1,
    yearTo: int = 2100,
    monthTo: int = 1,
    dayTo: int = 1,
) -> StatisticsSchema:
    """Get statistics for all dealers.

        Args:
        yearFrom: minimum year of parsing.
        monthFrom: minimum month of parsing.
        dayFrom: minimum day of parsing.
        yearTo: maximum year of parsing.
        monthTo: maximum month of parsing.
        dayTo: maximum day of parsing.

    Returns:
        All statistics information.
    """
    date_from = date_val(yearFrom, monthFrom, dayFrom)
    date_to = date_val(yearTo, monthTo, dayTo)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
    return StatisticsSchema.model_validate(
        await StatisticsDAO.get_general_stat(
            date_from,
            date_to,
        ),
    )


@router_v1.get('/statistics/{dealerId}')
async def dealer_static(
    dealerId: int,
    yearFrom: int = 1900,
    monthFrom: int = 1,
    dayFrom: int = 1,
    yearTo: int = 2100,
    monthTo: int = 1,
    dayTo: int = 1,
) -> StatisticsSchema:
    """Get dealer statistics.

        Args:
        dealerId: id of dealer.
        yearFrom: minimum year of parsing.
        monthFrom: minimum month of parsing.
        dayFrom: minimum day of parsing.
        yearTo: maximum year of parsing.
        monthTo: maximum month of parsing.
        dayTo: maximum day of parsing.

    Returns:
        Statistics corresponding to provided dealer.
    """
    date_from = date_val(yearFrom, monthFrom, dayFrom)
    date_to = date_val(yearTo, monthTo, dayTo)
    if (not date_from) or (not date_to):
        logger.error(DateError.detail)
        raise DateError
    dealer = await DealerDAO.find_by_id(dealerId)
    if not dealer:
        logger.error(DealerNotFound.detail)
        raise DealerNotFound
    return StatisticsSchema.model_validate(
        await StatisticsDAO.get_dealer_stat(
            dealerId,
            date_from,
            date_to,
        ),
    )


@router_v1.get('/product/{productKey}')
async def get_product(productKey: int) -> ProductValidationSchema:
    """Get product information by product-dealer connection key.

    Args:
        productKey: product-dealer connection key.

    Returns:
        Product data.
    """
    product_dealer = await ProductDealerDAO.find_one_or_none(key=productKey)
    if not product_dealer:
        logger.error(ProductDealerNotFound.detail)
        raise ProductDealerNotFound
    return ProductValidationSchema(
        **ProductSchema.model_validate(
            await ProductDAO.find_by_id(product_dealer.product_id),
        ).model_dump(),
    )


@router_v1.get('/testToken')
async def get_testLogin(
    user: User = Depends(get_current_user),
) -> List[DealerSchema]:
    """Get all dealers.

    Returns:
        All dealers data.
    """
    if not user:
        raise InvalidCredentialsException
    return await DealerDAO.find_all()
