from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Модель продукта."""

    __tablename__ = 'marketing_product'

    id: int = Field(..., alias='id')
    article: str = Field(..., alias='article')
    ean_13: int = Field(..., alias='ean13')
    name: str = Field(..., alias='name')
    cost: float = Field(..., alias='cost')
    recomended_price: float = Field(..., alias='recomendedPrice')
    category_id: int = Field(..., alias='categoryId')
    ozon_name: str = Field(..., alias='ozonName')
    name_1c: str = Field(..., alias='name1c')
    wb_name: str = Field(..., alias='wbName')
    ozon_article: int = Field(..., alias='ozonArticle')
    wb_article: int = Field(..., alias='wbArticle')
    ym_article: str = Field(..., alias='ymArticle')
    wb_article_td: str = Field(..., alias='wbArticleTd')

    class Config:
        orm_mode = True


class SNewProductDealerKey(BaseModel):
    """Модель связки продуктов."""

    key: str
    dealer_id: int
    product_id: int
