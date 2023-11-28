from pydantic import BaseModel


class ProductSchema(BaseModel):
    """Модель продукта."""

    __tablename__ = 'marketing_product'

    id: int
    article: str
    ean_13: int
    name: str
    cost: float
    recomended_price: float
    category_id: int
    ozon_name: str
    name_1c: str
    wb_name: str
    ozon_article: int
    wb_article: int
    ym_article: str
    wb_article_td: str

    class Config:
        orm_mode = True
