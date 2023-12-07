from sqlalchemy import (
    BigInteger,
    Boolean,
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
    """Dealer model."""

    __tablename__ = 'marketing_dealer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    product_dealer = relationship('ProductDealer', back_populates='dealer')
    parsed_data = relationship('ParsedProductDealer', back_populates='dealer')

    def __repr__(self) -> str:
        """Represent dealer model.

        Returns:
            Line with dealer name.
        """
        return f'Dealer {self.name}'


class Product(Base):
    """Product model."""

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
        """Represent the product model.

        Returns:
            Product name line.
        """
        return f'Product {self.name}'


class ProductDealer(Base):
    """Model of connection between dealer and product by key."""

    __tablename__ = 'marketing_productdealerkey'

    id = Column(Integer, primary_key=True)
    key = Column(Integer, unique=True, nullable=False)
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
        """Represent the product-dealer linkage model.

        Returns:
            String with product-dealer link key.
        """
        return f'Product {self.product_id} from the dealer {self.dealer_id}'


class ParsedProductDealer(Base):
    """Parsing data model."""

    __tablename__ = 'marketing_dealerprice'

    id = Column(Integer, primary_key=True)
    product_key = Column(Integer, ForeignKey('marketing_productdealerkey.key'))
    price = Column(Float)
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
    statistics = relationship('Statistics', back_populates='parsed_data')

    def __repr__(self) -> str:
        """Represent the parsing data model.

        Returns:
            String with the parsing data item id.
        """
        return f'Parsing data {self.id}'


class Statistics(Base):
    """Parsing statistics data model."""

    __tablename__ = 'marketing_statistics'

    id = Column(Integer, primary_key=True)
    parsed_data_id = Column(
        Integer,
        ForeignKey('marketing_dealerprice.id'),
        unique=True,
        nullable=False,
    )
    skipped = Column(Boolean, nullable=False, default=False)
    successfull = Column(Boolean, nullable=False, default=False)

    parsed_data = relationship(
        'ParsedProductDealer',
        back_populates='statistics',
    )

    def __repr__(self) -> str:
        """Represent the statistics model.

        Returns:
            String with the parsing product id.
        """
        return f'Statistics of parsed data {self.parsed_data_id}'
