from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, CheckConstraint, SmallInteger, Numeric
from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String(50), nullable=False, unique=True)
    name = Column(String(70), nullable=False)
    password = Column(String(255), nullable=False)
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
    name = Column(String(70), nullable=False)
    description = Column(Text, default='No description')
    price = Column(Numeric, nullable=False)
    quantity = Column(SmallInteger, default=0)
    available = Column(Boolean, default=False)

    user = relationship('User', back_populates='products')
    order = relationship('Order', back_populates='parent_product')


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('user.id', name='fk_client_order'))
    product_id = Column(Integer, ForeignKey('product.id', name='fk_product_order'))
    quantity = Column(SmallInteger, CheckConstraint('quantity > 0'), nullable=False)
    status = Column(Boolean, default=False)
    address = Column(String(100), nullable=False)
    observation = Column(String(70), default='No observation.')

    parent_user = relationship('User', back_populates='order')
    parent_product = relationship('Product', back_populates='order')
