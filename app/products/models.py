from sqlalchemy import Column, Integer, String, Float, URL, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Dealer(Base):
    __tablename__ = 'marketing_dealer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f'Dealer {self.name}'

class Product(Base):
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

    def __repr__(self):
        return f'Product {self.article}'

class ParsedProductDealer(Base):
    __tablename__ = 'marketing_dealerprice'

    id = Column(Integer, primary_key=True)
    product_key = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    product_url = Column(String)
    product_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    dealer_id = Column(Integer, ForeignKey('marketing_dealer.id'))

    def __repr__(self):
        return f'Parsed product {self.product_key}'
    
class ProductDealerAssociation(Base):
    __tablename__ = 'marketing_productdealerkey'

    id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    dealer_id = Column(Integer, ForeignKey('marketing_dealer.id'))
    product_id = Column(Integer, ForeignKey('marketing_product.id'))

