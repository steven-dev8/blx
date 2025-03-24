from fastapi import FastAPI, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.config.database import get_db, create_session_db
from src.schema.schemas import Product, User, UserResponse
from src.infra.sqlalchemy.repository.product import ProcessProduct
from src.infra.sqlalchemy.repository.user import ProcessUser

create_session_db()

app = FastAPI()


@app.post('/product', status_code=status.HTTP_201_CREATED, response_model=Product)
def add_product(product: Product, db: Session = Depends(get_db)):
    print(product)
    prd_db = ProcessProduct(db).create(product)
    return prd_db


@app.get('/product', status_code=status.HTTP_200_OK, response_model=List[Product])
def to_list_prds(db: Session = Depends(get_db)):
    list_prd = ProcessProduct(db).to_list()
    return list_prd


@app.get('/product/{id_query}', status_code=status.HTTP_200_OK, response_model=Product)
def query_product(id_query: int, db: Session = Depends(get_db)):
    result = ProcessProduct(db).search(id_query)
    if result:
        return result
    return Response(status_code=status.HTTP_404_NOT_FOUND, content='ID not found.')


@app.delete('/product/{id_prd}', status_code=status.HTTP_200_OK)
def del_product(id_prd: int, db: Session = Depends(get_db)):
    result = ProcessProduct(db).delete_product(id_prd)
    if result:
        return result
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="ID product not found")


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=User)
def add_user(user: User, db: Session = Depends(get_db)):
    user_db = ProcessUser(db).create(user)
    if user_db:
        return user_db
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content="User was not added,")


@app.get('/user', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def to_list_users(db: Session = Depends(get_db)):
    list_user = ProcessUser(db).to_list()
    if list_user:
        return list_user
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content='No users found')


@app.get('/user/{id_user}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def query_user(id_user: int, db: Session = Depends(get_db)):
    result_user = ProcessUser(db).query_user(id_user)
    if result_user:
        return result_user
    return Response(status_code=status.HTTP_404_NOT_FOUND, content='ID not found.')


@app.delete('/user/{id_user}', status_code=status.HTTP_200_OK)
def del_user(id_user: int, db: Session = Depends(get_db)):
    result = ProcessUser(db).delete_user(id_user)
    if result:
        return result
    return Response(status_code=status.HTTP_200_OK, content="ID not found")


@app.get('/user/products/')
def search_user_product(id_user: str, db: Session = Depends(get_db)):
    print('aqui')
    result = ProcessUser(db).user_product(id_user)
    return result


@app.put('/user/edit')
def edit_user(user: User, db: Session = Depends(get_db)):
    result = ProcessUser(db).edit_user(user)
    return result