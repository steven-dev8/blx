from fastapi import FastAPI, Depends, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.config.database import get_db, create_session_db
from src.schema.schemas import Product, User, UserResponse, ProductEdit
from src.infra.sqlalchemy.repository.product import ProcessProduct
from src.infra.sqlalchemy.repository.user import ProcessUser


create_session_db()

app = FastAPI()

origins = ["http://localhost",
           "http://localhost:8080",
           "http://localhost:8000"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_method=["*"],
                   allow_headers=["*"])


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


@app.put('/product/{id_prod}')
def edit_product(id_prod: int, product: ProductEdit, db: Session = Depends(get_db)):
    result = ProcessProduct(db).edit_product(id_prod, product)
    return result


@app.delete('/product/{id_prd}', status_code=status.HTTP_200_OK)
def del_product(id_prd: int, db: Session = Depends(get_db)):
    result = ProcessProduct(db).delete_product(id_prd)
    if result:
        return result
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="ID product not found")


# USERS

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
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


@app.get('/user/{id_user}/products')
def search_user_product(id_user: int, db: Session = Depends(get_db)):
    print('aqui')
    result = ProcessUser(db).user_product(id_user)
    return result


@app.put('/user/{id_user}')
def edit_user(id_user: int, user: User, db: Session = Depends(get_db)):
    result = ProcessUser(db).edit_user(id_user, user)
    return result