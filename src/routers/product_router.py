from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.product import ProcessProduct
from src.schema.schemas import Product, ProductEdit
from src.infra.sqlalchemy.config.database import get_db
from typing import List, Union


router = APIRouter()


@router.post('/product', status_code=status.HTTP_201_CREATED, response_model=Product)
def add_product(product: Product, session: Session = Depends(get_db)):
    prd_db = ProcessProduct(session).create(product)
    if not prd_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Body has an incorrect format.")
    return prd_db


@router.get('/product', status_code=status.HTTP_200_OK, response_model=List[Product] or ProductErro)
def to_list_prds(session: Session = Depends(get_db)):
    list_prd = ProcessProduct(session).to_list()
    if not list_prd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products registered.")
    return list_prd


@router.get('/product/{id_query}', status_code=status.HTTP_200_OK, response_model=Product)
def query_product(id_query: int, session: Session = Depends(get_db)):
    result = ProcessProduct(session).search(id_query)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The product with ID {id_query} was not found.")
    return result

@router.put('/product/{id_prod}')
def edit_product(id_prod: int, product: ProductEdit, session: Session = Depends(get_db)):
    result = ProcessProduct(session).edit_product(id_prod, product)
    if not result:
        raise HTTPException(status_code=400, detail="The Body has an incorrect format.")
    return result


@router.delete('/product/{id_prd}', status_code=status.HTTP_204_NO_CONTENT)
def del_product(id_prd: int, session: Session = Depends(get_db)):
    result = ProcessProduct(session).delete_product(id_prd)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The product with ID {id_prd} was not found.")
    return result