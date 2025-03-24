from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    number = Column(String, nullable=False)


    products = relationship('Product', back_populates='user')


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', name='fk_user'))
    name = Column(String, nullable=False)
    description = Column(Text, default='No description')
    price = Column(Float, nullable=False)
    avaliable = Column(Boolean, default=False)
    

    user = relationship('User', back_populates='products')