from datetime import date as datetype
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.core.schemas import to_snake_case


class ProductSchema(BaseModel):
    """Схема продукта."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )

    id: int
    article: str
    ean13: Optional[int]
    name: Optional[str]
    cost: Optional[float]
    recomendedPrice: Optional[float]
    categoryId: Optional[int]
    ozonName: Optional[str]
    name1c: Optional[str]
    wbName: Optional[str]
    ozonArticle: Optional[int]
    wbArticle: Optional[int]
    ymArticle: Optional[str]
    wbArticleTd: Optional[str]


class ParsedProductValidationSchema(BaseModel):
    """Схема данных парсинга."""

    id: int
    productKey: Optional[str]
    price: float
    productUrl: Optional[str]
    productName: str
    date: datetype
    dealerId: int


class ParsedProductSchema(ParsedProductValidationSchema):
    """Схема данных парсинга."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )


class MenuValidationSchema(BaseModel):
    """Схема меню данных парсинга."""

    items: List[ParsedProductValidationSchema]
    page: int
    size: int
    totalPage: int


class MenuSchema(MenuValidationSchema):
    """Схема меню данных парсинга."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    items: List[ParsedProductSchema]  # type: ignore[assignment]


class DealerSchema(BaseModel):
    """Схема дилера."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )

    id: int
    name: str


class RecomendationValidationSchema(BaseModel):
    """Схема рекомендуемого варианта."""

    id: int
    productName: str
    levenshteinDistance: int


class RecomendationSchema(RecomendationValidationSchema):
    """Схема рекомендуемого варианта."""

    model_config = ConfigDict(alias_generator=to_snake_case)


class ProductDealerKeySchema(BaseModel):
    """Модель связки продуктов."""

    id: int
    product_key: str
    product_name: str
    dealer_id: int


class UpdateParsedProductSchema(BaseModel):
    """Схема данных парсинга."""

    id: int
    productKey: Optional[str]
    productName: str
    dealerId: int


class UpdateProductDealerKey(BaseModel):
    """Модель для добавления связки продуктов."""

    msg: str
    newParsedProduct: List[UpdateParsedProductSchema]
    newProductDealer: List[ProductDealerKeySchema]


class UpdateSchema(UpdateProductDealerKey):
    """Схема обновленных данных парсинга."""

    newParsedProduct: List[UpdateParsedProductSchema]
    newProductDealer: List[ProductDealerKeySchema]

    class Config:
        alias_generator = to_snake_case
