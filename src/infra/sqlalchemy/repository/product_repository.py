from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schema.schemas import ProductBase, ProductCreate, ProductEdit, ProductResponse, ProductList, ProductAll
from src.infra.sqlalchemy.models import models
from src.infra.validators.product_validators import *
from src.infra.validators.product_validators import create_product as update_product


class ProcessProduct:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, product: ProductCreate, user_id: int):
        if not create_product(product):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The provided user data is invalid. Please check the input fields."
                )
        
        user_query = (
                      self.session.query(models.User.id)
                      .filter(models.User.id == user_id)
                      .first()
                      )

        if not user_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {product.user_id} was not found."
                )

        db_product = models.Product(**product.model_dump())
        db_product.user_id = user_id
        
        if avaliable_product(db_product.quantity):
            db_product.avaliable=True

        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return ProductResponse.model_validate(db_product)
     
    def list_user_product(self, user_id: int) -> list[ProductList]:
        products = (
                    self.session.query(models.Product)
                    .filter(models.Product.user_id == user_id)
                    .all()
                    )
        
        return [ProductList.model_validate(product) for product in products]

    def search(self, id_query: int) -> ProductAll:
        result = (
                  self.session.query(models.Product)
                  .filter(models.Product.id == id_query)
                  .first()
                  )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found."
                )

        return ProductAll.model_validate(result)

    def delete_product(self, id_prd: int):
        query = self.session.query(models.Product).filter(models.Product.id == id_prd).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {id_prd} was not found."
                )

        self.session.delete(query)
        self.session.commit()
    
    def edit_product(self, product: ProductEdit, prd_id: int, user_id: int):
        existing_product = (
                self.session.query(models.Product)
                .filter(models.Product.user_id == user_id,
                        models.Product.id == prd_id)
                .first()
                )
        
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found."
            )
        
        if not update_product(product):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The provided user data is invalid. Please check the input fields."
            )

        if product.name is not None:
            existing_product.name = product.name
        if product.description is not None:
            existing_product.description = product.description
        if product.price is not None:
            existing_product.price = product.price
        if product.quantity is not None:
            existing_product.quantity = product.quantity

        existing_product.avaliable = quantity_product(existing_product.quantity)

        self.session.commit()

