from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from src.infra.sqlalchemy.config.database import Base

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, default='No description')
    price = Column(Float, nullable=False)
    avaliable = Column(Boolean, default=False)