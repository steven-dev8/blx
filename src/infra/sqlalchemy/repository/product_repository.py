from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schema.schemas import ProductBase, ProductCreate, ProductEdit, ProductResponse, ProductList, ProductAll
from src.infra.sqlalchemy.models import models
from src.infra.validators.product_validators import *
from src.infra.validators.product_validators import create_product as update_product


class ProcessProduct:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, product: ProductCreate):
        if not create_product(product):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The provided user data is invalid. Please check the input fields."
                )
        
        user_query = self.session.query(models.User.id).filter(models.User.id == product.user_id).first()

        if not user_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {product.user_id} was not found."
                )

        db_product = models.Product(
                                    name=product.name,
                                    user_id=product.user_id,
                                    description=product.description,
                                    price=product.price,
                                    quantity=product.quantity,
                                    )
        
        if avaliable_product(db_product.quantity):
            db_product.avaliable=True

        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return ProductResponse.model_validate(db_product)
     
    def to_list(self):
        products = self.session.query(models.Product).all()
        if not products:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is unavailable. Fix in progress."
                )

        return [ProductList.model_validate(product) for product in products]

    def search(self, id_query: int):
        result = self.session.query(models.Product).filter(models.Product.id == id_query).first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {id_query} was not found."
                )

        return ProductAll.model_validate(result)

    def delete_product(self, id_prd: int):
        query = self.session.query(models.Product).filter(models.Product.id == id_prd).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {id_query} was not found."
                )

        self.session.delete(query)
        self.session.commit()
        return None
    
    def edit_product(self, id_user: int, product: ProductEdit):
        if not update_product(product):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The product with ID {id_user} was not found."
            )

        query = self.session.query(models.Product).filter(models.Product.id == id_user).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {id_user} was not found."
            )

        query.name = product.name
        query.description = product.description
        query.price = product.price
        query.quantity = product.quantity
        if quantity_product(query.quantity):
            query.avaliable = True

        self.session.commit()
        self.session.refresh(query)
        return None
