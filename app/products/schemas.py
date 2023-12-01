from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Модель продукта."""

    __tablename__ = 'marketing_product'

    id: int = Field(..., alias='id')
    article: str = Field(..., alias='article')
    ean_13: int = Field(..., alias='ean_13')
    name: str = Field(..., alias='name')
    cost: float = Field(..., alias='cost')
    recomended_price: float = Field(..., alias='recomended_price')
    category_id: int = Field(..., alias='category_id')
    ozon_name: str = Field(..., alias='ozon_name')
    name_1c: str = Field(..., alias='name_1c')
    wb_name: str = Field(..., alias='wb_name')
    ozon_article: int = Field(..., alias='ozon_article')
    wb_article: int = Field(..., alias='wb_article')
    ym_article: str = Field(..., alias='ym_article')
    wb_article_td: str = Field(..., alias='wb_article_td')

    class Config:
        orm_mode = True
