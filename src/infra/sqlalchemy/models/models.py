from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    number = Column(String, nullable=False)

    products = relationship('Product', back_populates='user')
    order = relationship('Order', back_populates='parent_user')


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

    parent_user = relationship('User', back_populates='order')
    parent_product = relationship('Product', back_populates='order')
