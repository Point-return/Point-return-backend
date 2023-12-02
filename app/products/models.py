from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.models import Base


class Dealer(Base):
    """Модель дилера."""

    __tablename__ = 'marketing_dealer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    product_dealer = relationship('ProductDealer', back_populates='dealer')
    parsed_data = relationship('ParsedProductDealer', back_populates='dealer')

    def __repr__(self) -> str:
        """Функция для представления модели дилера.

        Returns:
            Строку с именем дилера.
        """
        return f'Дилер {self.name}'


class Product(Base):
    """Модель продукта."""

    __tablename__ = 'marketing_product'

    id = Column(Integer, primary_key=True)
    article = Column(String, nullable=False, unique=True)
    ean_13 = Column(BigInteger)
    name = Column(String)
    cost = Column(Float)
    recommended_price = Column(Float)
    category_id = Column(Integer)
    ozon_name = Column(String)
    name_1c = Column(String)
    wb_name = Column(String)
    ozon_article = Column(Integer)
    wb_article = Column(Integer)
    ym_article = Column(String)
    wb_article_td = Column(String)

    product_dealer = relationship('ProductDealer', back_populates='product')

    def __repr__(self) -> str:
        """Функция для представления модели продукта.

        Returns:
            Строку с названием продукта.
        """
        return f'Продукт {self.name}'


class ProductDealer(Base):
    """Модель связи дилера и продукта по ключу."""

    __tablename__ = 'marketing_productdealerkey'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    dealer_id = Column(
        Integer,
        ForeignKey('marketing_dealer.id'),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey('marketing_product.id'),
        nullable=False,
    )

    parsed_data = relationship(
        'ParsedProductDealer',
        back_populates='product_dealer',
    )
    product = relationship('Product', back_populates='product_dealer')
    dealer = relationship('Dealer', back_populates='product_dealer')

    def __repr__(self) -> str:
        """Функция для представления модели связки продукт-дилер.

        Returns:
            Строку с ключом связки продукт-дилер.
        """
        return f'Продукт {self.product_id} от дилера {self.dealer_id}'


class ParsedProductDealer(Base):
    """Модель данных парсинга."""

    __tablename__ = 'marketing_dealerprice'

    id = Column(Integer, primary_key=True)
    product_key = Column(String, ForeignKey('marketing_productdealerkey.key'))
    price = Column(Float, nullable=False)
    product_url = Column(String)
    product_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    dealer_id = Column(
        Integer,
        ForeignKey('marketing_dealer.id'),
        nullable=False,
    )

    product_dealer = relationship(
        'ProductDealer',
        back_populates='parsed_data',
    )
    dealer = relationship('Dealer', back_populates='parsed_data')

    def __repr__(self) -> str:
        """Функция для представления модели данных парсинга.

        Returns:
            Строку с ключом продукта парсинга.
        """
        return f'Данные парсинга {self.product_key}'
