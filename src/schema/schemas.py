from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    name: str
    password: str
    number: str


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    avaliable: bool = False

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: Optional[str] = None
    quantity: int
    status: bool = True
    address: str
    obs: Optional[str] = "No observation"
