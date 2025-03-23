from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: int
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


class Product(BaseModel):
    id: Optional[str] = None
    user_id: int
    name: str
    description: str
    price: float
    avaliable: bool = False

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: Optional[str] = None
    quantity: int
    status: bool = True
    address: str
    obs: Optional[str] = "No observation"
