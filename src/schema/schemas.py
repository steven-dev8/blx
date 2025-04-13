from typing import Optional, List
from pydantic import BaseModel


# USER
class UserBase(BaseModel):
    name: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserLoginOut(UserBase):
    id: int
    number: str


class UserCreate(UserBase):
    login: str
    password: str
    number: str


class UserEdit(BaseModel):
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    number: Optional[str] = None


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


class ProductEdit(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductCreate(ProductBase):
    ...


class ProductResponse(ProductBase):
    available: bool

    class Config:
        from_attributes=True


class ProductList(ProductResponse):
    id: int


class ProductAll(ProductResponse, ProductCreate):
    pass


#ORDER
class OrderBase(BaseModel):
    quantity: int
    status: Optional[bool] = False
    address: str
    observation: Optional[str] = "No observation."


class OrderCreate(OrderBase):
    product_id: int

    class Config:
        from_attributes=True

class OrderResponse(OrderBase):
    product_id: Optional[int]
    id: int

    class Config:
        from_attributes=True

class OrderUserSearch(OrderResponse):
    pass