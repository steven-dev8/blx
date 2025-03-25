from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.user import ProcessUser
from src.schema.schemas import User, UserProduct, UserResponse
from src.infra.sqlalchemy.config.database import get_db
from typing import List


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def add_user(user: User, db: Session = Depends(get_db)):
    user_db = ProcessUser(db).create(user)
    if user_db:
        return user_db
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content="User was not added,")


@router.get('/user', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def to_list_users(db: Session = Depends(get_db)):
    list_user = ProcessUser(db).to_list()
    if list_user:
        return list_user
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content='No users found')


@router.get('/user/{id_user}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def query_user(id_user: int, db: Session = Depends(get_db)):
    result_user = ProcessUser(db).query_user(id_user)
    if result_user:
        return result_user
    return Response(status_code=status.HTTP_404_NOT_FOUND, content='ID not found.')


@router.delete('/user/{id_user}', status_code=status.HTTP_200_OK)
def del_user(id_user: int, db: Session = Depends(get_db)):
    result = ProcessUser(db).delete_user(id_user)
    if result:
        return result
    return Response(status_code=status.HTTP_200_OK, content="ID not found")


@router.get('/user/{id_user}/products')
def search_user_product(id_user: int, db: Session = Depends(get_db)):
    print('aqui')
    result = ProcessUser(db).user_product(id_user)
    return result


@router.put('/user/{id_user}')
def edit_user(id_user: int, user: User, db: Session = Depends(get_db)):
    result = ProcessUser(db).edit_user(id_user, user)
    return result