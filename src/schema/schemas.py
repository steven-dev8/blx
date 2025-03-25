from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    name: str
    password: str
    number: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    number: str

    class Config:
        from_attributes = True


class UserProduct(BaseModel):
    id: int
    name: str
    products: List["Product"]


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    avaliable: bool = False
    user_id: int


    class Config:
        from_attributes = True


class ProductEdit(BaseModel):
    name: str
    description: str
    price: float
    avaliable: bool = False


class Order(BaseModel):
    id: Optional[str]
    quantity: int
    status: bool = True
    address: str
    obs: Optional[str] = "No observation"
