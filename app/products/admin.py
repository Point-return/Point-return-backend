# mypy: disable-error-code="list-item, assignment"
from sqladmin import ModelView

from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
    Statistics,
)


class DealerAdmin(ModelView, model=Dealer):
    """Presentation of the dealer model in the admin area."""

    column_list = (Dealer.id, Dealer.name, Dealer.product_dealer)
    column_searchable_list = (Dealer.name,)
    column_sortable_list = (Dealer.id, Dealer.name)
    icon = 'fa-solid fa-user-tie'
    name = 'Dealer'
    name_plural = 'Dealers'


class ProductAdmin(ModelView, model=Product):
    """Presentation of the product model in the admin area."""

    column_list = tuple(Product.__table__.columns) + (Product.product_dealer,)
    column_searchable_list = (Product.name,)
    column_sortable_list = (
        Product.id,
        Product.name,
    )
    icon = 'fa-solid fa-barcode'
    name = 'Product'
    name_plural = 'Products'


class ProductDealerAdmin(ModelView, model=ProductDealer):
    """Presentation of the product-dealer model in the admin area."""

    column_list = [
        ProductDealer.id,
        ProductDealer.key,
        ProductDealer.product_id,
        ProductDealer.dealer_id,
        ProductDealer.product,
        ProductDealer.dealer,
        ProductDealer.parsed_data,
    ]
    column_searchable_list = (ProductDealer.key,)
    column_sortable_list = (
        ProductDealer.id,
        ProductDealer.key,
    )
    icon = 'fa-solid fa-file-contract'
    name = 'Product-dealer connection'
    name_plural = 'Product-dealer connections'


class ParsedProductDealerAdmin(ModelView, model=ParsedProductDealer):
    """Representation of the parsing data model in the admin area."""

    column_list = tuple(ParsedProductDealer.__table__.columns) + (
        ParsedProductDealer.dealer,
        ParsedProductDealer.product_dealer,
    )
    column_sortable_list = (
        ParsedProductDealer.id,
        ParsedProductDealer.date,
        ParsedProductDealer.product_key,
    )
    icon = 'fa-regular fa-circle-down'
    name = 'Parsing data'
    name_plural = 'Parsing data'


class StatisticsAdmin(ModelView, model=Statistics):
    """Statistics representation in admin zone."""

    column_list = tuple(Statistics.__table__.columns) + (
        Statistics.parsed_data,
    )
    column_sortable_list = (
        Statistics.id,
        Statistics.parsed_data_id,
        Statistics.skipped,
        Statistics.successfull,
    )
    icon = 'fa-solid fa-chart-simple'
    name = 'Statistic'
    name_plural = 'Statistics'
