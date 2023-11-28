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

    column_list = [Dealer.id, Dealer.name]
    name = 'Дилер'
    name_plural = 'Дилеры'


class ProductAdmin(ModelView, model=Product):
    """Представление модели дилера в админ-зоне."""

    column_list = Product.__table__.columns
    name = 'Продукт'
    name_plural = 'Продукты'


class ProductDealerAdmin(ModelView, model=ProductDealer):
    """Представление модели дилера в админ-зоне."""

    column_list = [
        ProductDealer.id,
        ProductDealer.key,
        ProductDealer.product_id,
        ProductDealer.dealer_id,
    ]
    name = 'Связь продукта и дилера'
    name_plural = 'Связи продукта и дилера'


class ParsedProductDealerAdmin(ModelView, model=ParsedProductDealer):
    """Представление модели дилера в админ-зоне."""

    column_list = ParsedProductDealer.__table__.columns
    name = 'Данные парсинга'
    name_plural = 'Данные парсинга'
