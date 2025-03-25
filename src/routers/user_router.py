from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.user import ProcessUser
from src.schema.schemas import User, UserProduct, UserResponse
from src.infra.sqlalchemy.config.database import get_db
from typing import List, Union


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def add_user(user: User, session: Session = Depends(get_db)):
    user_db = ProcessUser(session).create(user)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The Body has an incorrect format.")
    return user_db


@router.get('/user', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def to_list_users(session: Session = Depends(get_db)):
    list_user = ProcessUser(session).to_list()
    if not list_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No users registered.")
    return list_user

@router.get('/user/{id_user}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def query_user(id_user: int, session: Session = Depends(get_db)):
    result_user = ProcessUser(session).query_user(id_user)
    if not result_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with ID {id_user} was not found.")
    return result_user

@router.delete('/user/{id_user}', status_code=status.HTTP_200_OK)
def del_user(id_user: int, session: Session = Depends(get_db)):
    result = ProcessUser(session).delete_user(id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with ID {id_user} was not found.")
    return result

@router.get('/user/{id_user}/products')
def search_user_product(id_user: int, session: Session = Depends(get_db)):
    result = ProcessUser(session).user_product(id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with ID {id_user} was not found.")
    return result


@router.put('/user/{id_user}')
def edit_user(id_user: int, user: User, session: Session = Depends(get_db)):
    result = ProcessUser(session).edit_user(id_user, user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with ID {id_user} was not found.")
    return result