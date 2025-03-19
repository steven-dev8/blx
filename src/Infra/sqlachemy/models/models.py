from sqlachemy import Column, Integer, String, Float, Boolean, Text
from src.Infra.sqlachemy.config.database import Base

class Product(Base):
    __tablename__ = 'product'

    id_prd = Column(Integer, primary_key=True, index=true)
    name = Column(String, nullable=False),
    description = Column(String, default='No description')
    price = Column(Float, nullable=False)
    avaliable = Column(Boolean, default=True)