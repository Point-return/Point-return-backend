from sqlalchemy import Column, Integer, String

from app.database import Base


class Dealers(Base):
    __tablename__ = 'marketing_dealer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
