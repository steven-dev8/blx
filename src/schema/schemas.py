from typing import Optional, List, Union
from pydantic import BaseModel


# USER
class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    login: str
    password: str
    number: str


class UserEdit(UserCreate):
    pass


class UserResponse(UserBase):
    number: Optional[str] = None
    id: int

    class Config:
        from_attributes=True


class UserProduct(UserBase):
    id: int
    products: List["ProductResponse"]

    class Config:
        from_attributes = True


# PRODUCT
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    user_id: int


class ProductResponse(ProductBase):
    avaliable: bool

    class Config:
        from_attributes=True


class ProductList(ProductResponse):
    id: int

class ProductAll(ProductResponse, ProductCreate):
    pass

class ProductEdit(ProductBase):
    pass


#ORDER
class OrderBase(BaseModel):
    quantity: int
    status: Optional[bool] = False
    address: str
    observation: Optional[str] = "No observation."


class OrderCreate(OrderBase):
    client_id: int
    product_id: int

    class Config:
        from_attributes=True

class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes=True

class OrderResponseSearch(OrderCreate):
    id: int

    class Config:
        from_attributes=True

class OrderUserSearch(OrderResponseSearch):
    pass