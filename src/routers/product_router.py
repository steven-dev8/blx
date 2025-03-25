from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.product import ProcessProduct
from src.schema.schemas import Product, ProductEdit
from src.infra.sqlalchemy.config.database import get_db
from typing import List


router = APIRouter()


@router.post('/product', status_code=status.HTTP_201_CREATED, response_model=Product)
def add_product(product: Product, db: Session = Depends(get_db)):
    print(product)
    prd_db = ProcessProduct(db).create(product)
    return prd_db


@router.get('/product', status_code=status.HTTP_200_OK, response_model=List[Product])
def to_list_prds(db: Session = Depends(get_db)):
    list_prd = ProcessProduct(db).to_list()
    return list_prd


@router.get('/product/{id_query}', status_code=status.HTTP_200_OK, response_model=Product)
def query_product(id_query: int, db: Session = Depends(get_db)):
    result = ProcessProduct(db).search(id_query)
    if result:
        return result
    return Response(status_code=status.HTTP_404_NOT_FOUND, content='ID not found.')


@router.put('/product/{id_prod}')
def edit_product(id_prod: int, product: ProductEdit, db: Session = Depends(get_db)):
    result = ProcessProduct(db).edit_product(id_prod, product)
    return result


@router.delete('/product/{id_prd}', status_code=status.HTTP_200_OK)
def del_product(id_prd: int, db: Session = Depends(get_db)):
    result = ProcessProduct(db).delete_product(id_prd)
    if result:
        return result
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="ID product not found")