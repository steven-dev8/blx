from typing import Optional, List
from pydantic import BaseModel


# USER
class UserBase(BaseModel):
    name: str
    number: str


class UserCreate(UserBase):
    login: str
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes=True


# PRODUCT
class UserProduct(UserBase):
    products: List[Product]


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    user_id: int


class ProductResponse(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes=True


class ProductEdit(ProductBase):
    pass


#ORDER
class OrderBase(BaseModel):
    quantity: int
    status: bool = False
    address: str
    obs: Optional[str] = "No observation."


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int

    class Config:
        from_attributes=True