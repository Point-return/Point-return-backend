from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from app.core.models import Base


class Dealer(Base):
    """Модель дилера."""

    __tablename__ = 'marketing_dealer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        """Функция для представления модели дилера.

        Returns:
            Строку с именем дилера.
        """
        return f'Dealer {self.name}'


class Product(Base):
    """Модель продукта."""

    __tablename__ = 'marketing_product'

    id = Column(Integer, primary_key=True)
    article = Column(String, nullable=False)
    ean_13 = Column(Integer)
    name = Column(String)
    cost = Column(Float)
    recomended_price = Column(Float)
    category_id = Column(Integer)
    ozon_name = Column(String)
    name_1c = Column(String)
    wb_name = Column(String)
    ozon_article = Column(Integer)
    wb_article = Column(Integer)
    ym_article = Column(String)
    wb_article_td = Column(String)

    def __repr__(self) -> str:
        """Функция для представления модели продукта.

        Returns:
            Строку с названием продукта.
        """
        return f'Product {self.name}'


class ParsedProductDealer(Base):
    """Модель данных парсинга."""

    __tablename__ = 'marketing_dealerprice'

    id = Column(Integer, primary_key=True)
    product_key = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    product_url = Column(String)
    product_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    dealer_id = Column(Integer, ForeignKey('marketing_dealer.id'))

    def __repr__(self) -> str:
        """Функция для представления модели данных парсинга.

        Returns:
            Строку с ключом продукта парсинга.
        """
        return f'Данные парсинга {self.product_key}'


class ProductDealer(Base):
    """Модель связи дилера и продукта по ключу."""

    __tablename__ = 'marketing_productdealerkey'

    id = Column(Integer, primary_key=True)
    key = Column(Integer, ForeignKey('marketing_dealerprice.id'))
    dealer_id = Column(Integer, ForeignKey('marketing_dealer.id'))
    product_id = Column(Integer, ForeignKey('marketing_product.id'))

    def __repr__(self) -> str:
        """Функция для представления модели связки продукт-дилер.

        Returns:
            Строку с ключом связки продукт-дилер.
        """
        return (
            f'Продукт {self.product_id} от дилера '
            f'{self.dealer_id} по ключу {self.key}'
        )
