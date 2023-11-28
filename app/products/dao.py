from app.core.dao import BaseDAO
from app.products.models import (
    Dealer,
    ParsedProductDealer,
    Product,
    ProductDealer,
)


class ProductDAO(BaseDAO):
    """Интерфейс работы с моделями продуктов."""

    model = Product


class ProductDealerDAO(BaseDAO):
    """Интерфейс работы с моделями связок продукт-дилер."""

    model = ProductDealer


class DealerDAO(BaseDAO):
    """Интерфейс работы с моделями дилеров."""

    model = Dealer


class ParsedProductDealerDAO(BaseDAO):
    """Интерфейс работы с моделями данных парсинга."""

    model = ParsedProductDealer
