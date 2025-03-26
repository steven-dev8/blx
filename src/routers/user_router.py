from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.user_repository import ProcessUser
from src.schema.schemas import UserProduct, UserResponse, UserBase, UserCreate, UserEdit
from src.infra.sqlalchemy.config.database import get_db
from typing import List, Union


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def add_user(user: UserCreate, session: Session = Depends(get_db)):
    user_db = ProcessUser(session).create(user)
    return user_db


@router.get('/user', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def to_list_users(session: Session = Depends(get_db)):
    list_user = ProcessUser(session).to_list()
    return list_user


@router.get('/user/{id_user}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def query_user(id_user: int, session: Session = Depends(get_db)):
    result_user = ProcessUser(session).query_user(id_user)
    return result_user


@router.delete('/user/{id_user}', status_code=status.HTTP_204_NO_CONTENT)
def del_user(id_user: int, session: Session = Depends(get_db)):
    result = ProcessUser(session).delete_user(id_user)
    return None


@router.get('/user/{id_user}/products', status_code=status.HTTP_200_OK, response_model=UserProduct)
def search_user_product(id_user: int, session: Session = Depends(get_db)):
    result = ProcessUser(session).user_product(id_user) 
    return result


@router.put('/user/{id_user}', status_code=status.HTTP_204_NO_CONTENT)
def edit_user(id_user: int, user: UserEdit, session: Session = Depends(get_db)):
    result = ProcessUser(session).edit_user(id_user, user)
    return result