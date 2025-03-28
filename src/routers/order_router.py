from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.repository.order_repository import ProcessOrder
from src.schema.schemas import OrderCreate
from src.infra.sqlalchemy.config.database import get_db


router = APIRouter()


@router.post('/order', status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, session: Session = Depends(get_db)):
    result = ProcessOrder(session).create_order(order)
    return result