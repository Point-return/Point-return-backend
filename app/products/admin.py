# mypy: disable-error-code="list-item, assignment"
from sqladmin import ModelView

from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
)


class DealerAdmin(ModelView, model=Dealer):
    """Представление модели дилера в админ-зоне."""

    column_list = (Dealer.id, Dealer.name, Dealer.product_dealer)
    column_searchable_list = (Dealer.name,)
    column_sortable_list = (Dealer.id, Dealer.name)
    icon = 'fa-solid fa-user-tie'
    name = 'Дилер'
    name_plural = 'Дилеры'


class ProductAdmin(ModelView, model=Product):
    """Представление модели дилера в админ-зоне."""

    column_list = tuple(Product.__table__.columns) + (Product.product_dealer,)
    column_searchable_list = (Product.name,)
    column_sortable_list = (
        Product.id,
        Product.name,
    )
    icon = 'fa-solid fa-barcode'
    name = 'Продукт'
    name_plural = 'Продукты'


class ProductDealerAdmin(ModelView, model=ProductDealer):
    """Представление модели дилера в админ-зоне."""

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
    name = 'Связь продукта и дилера'
    name_plural = 'Связи продукта и дилера'


class ParsedProductDealerAdmin(ModelView, model=ParsedProductDealer):
    """Представление модели дилера в админ-зоне."""

    column_list = tuple(ParsedProductDealer.__table__.columns) + (
        ParsedProductDealer.dealer,
        ParsedProductDealer.product_dealer,
    )
    column_sortable_list = (ParsedProductDealer.id, ParsedProductDealer.date)
    icon = 'fa-regular fa-circle-down'
    name = 'Данные парсинга'
    name_plural = 'Данные парсинга'
