from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    name: str
    password: str
    number: str
    my_product = List[Product]
    my_orders = List[Order]


class Product(BaseModel):
    id: Optional[str] = None
    user: User
    name: str
    description: str
    price: float
    avaliable: bool = False
