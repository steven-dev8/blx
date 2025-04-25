from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.repository.order_repository import ProcessOrder
from src.schema.schemas import OrderCreate, OrderResponse, OrderResponse, UserLoginOut
from src.routers.auth_utils import get_registered_user
from src.infra.sqlalchemy.config.database import get_db


router = APIRouter()


@router.post('/order', status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_client_order(order: OrderCreate,
                 user: UserLoginOut = Depends(get_registered_user),
                 session: Session = Depends(get_db)):
    result = ProcessOrder(session).create_order(order, user.id)
    return result


@router.get('/order/client', status_code=status.HTTP_200_OK, response_model=List[OrderResponse], tags=["Orders"])
def list_client_orders(user: UserLoginOut = Depends(get_registered_user),
               session: Session = Depends(get_db)):
    result = ProcessOrder(session).list_user_order(user.id)
    return result


@router.get('/order/client/{id_order}', status_code=status.HTTP_200_OK, response_model=OrderResponse, tags=["Orders"])
def search_client_order(id_order: int,
                 user: UserLoginOut = Depends(get_registered_user),
                 session: Session = Depends(get_db)):
    result = ProcessOrder(session).search_order(id_order, user.id)
    return result


@router.delete('/order/client/{id_order}', status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
def delete_client_order(id_order: int,
                 user: UserLoginOut = Depends(get_registered_user),
                 session: Session = Depends(get_db)):
    ProcessOrder(session).delete_order(id_order, user.id)


@router.get('/order/vendor/{id_order}', status_code=status.HTTP_200_OK, response_model=OrderResponse, tags=["Orders"])
def search_vendor_orders(id_order: int,
                         user: UserLoginOut = Depends(get_registered_user),
                         session: Session = Depends(get_db)):
    order = ProcessOrder(session).search_vendor_order(id_order, user.id)
    return order



@router.patch('/order/{id_order}', status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
def change_status(id_order: int,
                  status: bool = False,
                  user: UserLoginOut = Depends(get_registered_user),
                  session: Session = Depends(get_db)):
    result = ProcessOrder(session).change_status(id_order, user.id, status)
    return result
