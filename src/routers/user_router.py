from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.repository.user_repository import ProcessUser
from src.schema.schemas import UserProduct, UserResponse, UserEdit, UserLoginOut
from src.infra.sqlalchemy.config.database import get_db
from src.routers.auth_utils import get_registered_user


router = APIRouter()


@router.delete('/user', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def del_user(user: UserLoginOut = Depends(get_registered_user),
             session: Session = Depends(get_db)):
    ProcessUser(session).delete_user(user.id)


@router.put('/user', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def edit_user(user_edit: UserEdit,
              user: UserLoginOut = Depends(get_registered_user),
              session: Session = Depends(get_db)):
    ProcessUser(session).edit_user(user.id, user_edit)


@router.get('/user/orders', status_code=status.HTTP_200_OK, tags=["Users"])
def list_orders(user: UserLoginOut = Depends(get_registered_user),
                session: Session = Depends(get_db)):
    result = ProcessUser(session).user_order(user.id)
    return result
