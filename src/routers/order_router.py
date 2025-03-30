from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.repository.order_repository import ProcessOrder
from src.schema.schemas import OrderCreate, OrderResponse, OrderResponseSearch
from src.infra.sqlalchemy.config.database import get_db


router = APIRouter()


@router.post('/order', status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, session: Session = Depends(get_db)):
    result = ProcessOrder(session).create_order(order)
    return result


@router.get('/order', status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
def list_order(session: Session = Depends(get_db)):
    result = ProcessOrder(session).list_order()
    return result


@router.get('/order/{id_order}', status_code=status.HTTP_200_OK, response_model=OrderResponseSearch)
def search_order(id_order: int, session: Session = Depends(get_db)):
    result = ProcessOrder(session).search_order(id_order)
    return result


@router.delete('/order/{id_order}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id_order: int, session: Session = Depends(get_db)):
    result = ProcessOrder(session).delete_order(id_order)
    return result


@router.patch('/order/{id_order}', status_code=status.HTTP_204_NO_CONTENT)
def change_status(id_order: int, status: bool = False, session: Session = Depend(get_db)):
    result = ProcessOrder(session).change_status(id_order, status)
    return result