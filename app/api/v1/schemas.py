from datetime import date as datetype
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.core.schemas import to_snake_case


class ProductValidationSchema(BaseModel):
    """Product validation schema."""

    id: int
    article: str
    ean13: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = None
    recomendedPrice: Optional[float] = None
    categoryId: Optional[int] = None
    ozonName: Optional[str] = None
    name1c: Optional[str] = None
    wbName: Optional[str] = None
    ozonArticle: Optional[int] = None
    wbArticle: Optional[int] = None
    ymArticle: Optional[str] = None
    wbArticleTd: Optional[str] = None


class ProductSchema(ProductValidationSchema):
    """Product schema."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )


class ParsedProductValidationSchema(BaseModel):
    """Parsing data validation schema."""

    id: int
    productKey: Optional[int] = None
    price: float
    productUrl: Optional[str] = None
    productName: str
    date: datetype
    dealerId: int


class ParsedProductSchema(ParsedProductValidationSchema):
    """Parsing data schema."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )


class MenuValidationSchema(BaseModel):
    """Parsing data menu validation schema."""

    items: List[ParsedProductValidationSchema]
    page: int
    size: int
    totalPage: int


class MenuSchema(MenuValidationSchema):
    """Parsing data menu schema."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    items: List[ParsedProductSchema]  # type: ignore[assignment]


class DealerSchema(BaseModel):
    """Dealer schema."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )

    id: int
    name: str


class RecomendationValidationSchema(BaseModel):
    """Validation schema of the recommended option."""

    id: int
    productName: str
    levenshteinDistance: int


class RecomendationSchema(RecomendationValidationSchema):
    """Schema of the recommended option."""

    model_config = ConfigDict(alias_generator=to_snake_case)


class StatisticsSchema(BaseModel):
    """Statistic schema."""

    QuantitySuccessfull: int
    QuantitySkipped: int
    percent: str
