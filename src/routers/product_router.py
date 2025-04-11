from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.repository.product_repository import ProcessProduct
from src.schema.schemas import ProductCreate, ProductEdit, ProductResponse, ProductList, ProductAll, UserLoginOut
from src.routers.auth_utils import get_registered_user
from src.infra.sqlalchemy.config.database import get_db


router = APIRouter()


@router.post('/product', status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def add_product(product: ProductCreate,
                user: UserLoginOut = Depends(get_registered_user),
                session: Session = Depends(get_db)):
    prd_db = ProcessProduct(session).create(product, user.id)
    return prd_db


@router.get('/product', status_code=status.HTTP_200_OK, response_model=List[ProductList])
def to_list_prds(session: Session = Depends(get_db)):
    list_prd = ProcessProduct(session).to_list()
    return list_prd


@router.get('/product/{id_query}', status_code=status.HTTP_200_OK, response_model=ProductAll)
def query_product(id_query: int, session: Session = Depends(get_db)):
    result = ProcessProduct(session).search(id_query)
    return result


@router.put('/product/{id_prod}', status_code=status.HTTP_204_NO_CONTENT)
def edit_product(id_prod: int, product: ProductEdit, session: Session = Depends(get_db)):
    result = ProcessProduct(session).edit_product(id_prod, product)
    return result


@router.delete('/product/{id_prd}', status_code=status.HTTP_204_NO_CONTENT)
def del_product(id_prd: int, session: Session = Depends(get_db)):
    result = ProcessProduct(session).delete_product(id_prd)
    return result
