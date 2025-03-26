from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base
from typing import List


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String(50), nullable=False, unique=True)
    name = Column(String(70), nullable=False)
    password = Column(String(30), nullable=False)
    number = Column(String(11), nullable=False)

    products = relationship('Product', back_populates='user', cascade="all, delete-orphan")
    order = relationship('Order', back_populates='parent_user')

    __table_args__ = (
        CheckConstraint('LENGTH(login) >= 5', name='chk_login'),
    )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', name='fk_user'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, default='No description')
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    avaliable = Column(Boolean, default=False)

    user = relationship('User', back_populates='products')
    order = relationship('Order', back_populates='parent_product')


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('user.id', name='fk_client_order'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id', name='fk_product_order'), nullable=False)
    quantity = Column(Integer, CheckConstraint('quantity > 0'), nullable=False)
    status = Column(Boolean, default=False)
    address = Column(String, nullable=False)
    observation = Column(String, default='No observation.')

    parent_user = relationship('User', back_populates='order')
    parent_product = relationship('Product', back_populates='order')
