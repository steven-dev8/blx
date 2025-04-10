from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models import models
from src.schema.schemas import OrderBase, OrderResponseSearch, OrderCreate, OrderResponse
import src.infra.validators.order_validators as validator

class ProcessOrder:
    def __init__(self, session: Session):
        self.session = session
    
    def create_order(self, order: OrderCreate, user_id: int):
        product = self.session.query(models.Product).filter(
                                models.Product.id == order.product_id
                                ).scalar()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {order.product_id} was not found."
            )
            
        if validator.additional_check(order, product.quantity):
            quantity = product.quantity - order.quantity
            product.quantity = quantity

            if quantity == 0:
                product.avaliable = False

        new_order = models.Order(**order.model_dump())
        new_order.client_id = user_id
        
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        return OrderResponse.model_validate(new_order)
    
    def list_order(self):
        result = self.session.query(models.Order).all()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is unavailable. Fix in progress."
                )
        
        return [OrderResponse.model_validate(order_valid) for order_valid in result]

    def search_order(self, id_order: int):
        query = self.session.query(models.Order).filter(models.Order.id == id_order).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The order with ID {id_order} was not found."
            )

        return OrderResponseSearch.model_validate(query)
    
    def delete_order(self, id_order: int):
        order = self.session.query(models.Order).filter(models.Order.id == id_order).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The order with ID {id_order} was not found.'
            )

        self.session.delete(order)
        self.session.commit()
        return None
    
    def change_status(self, id_order: int, status: bool):
        query = self.session.query(models.Order).filter(models.Order.id == id_order).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The order with ID {id_order} was not found.'
            )
        
        query.status = status
        self.session.commit()
        return None