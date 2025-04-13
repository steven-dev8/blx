from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models import models
from src.schema.schemas import OrderResponse, OrderCreate, OrderResponse
import src.infra.validators.order_validators as validator

class ProcessOrder:
    def __init__(self, session: Session):
        self.session = session
    
    def create_order(self, order: OrderCreate, user_id: int):
        product = (
                    self.session.query(models.Product)
                   .filter(models.Product.id == order.product_id)
                   .first()
                   )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {order.product_id} was not found."
            )
        
        if product.user_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot purchase your own product."
            )
            
        if validator.additional_check(order, product.quantity):
            quantity = product.quantity - order.quantity
            product.quantity = quantity

            if quantity == 0:
                product.available = False

        new_order = models.Order(**order.model_dump())
        new_order.client_id = user_id
        
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        return OrderResponse.model_validate(new_order)
    
    def list_user_order(self, user_id: int) -> list[OrderResponse]:
        result = (
                  self.session.query(models.Order)
                  .filter(models.Order.client_id == user_id)
                  .all()
                  )

        return [OrderResponse.model_validate(order_valid) for order_valid in result]

    def search_order(self, id_order: int, user_id) -> OrderResponse:
        order = (
                self.session.query(models.Order)
                .filter(models.Order.client_id == user_id,
                        models.Order.id == id_order)
                        .first()
                )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The order with ID {id_order} was not found."
            )

        return OrderResponse.model_validate(order)
    
    def delete_order(self, order_id: int, user_id):
        order = (
                self.session.query(models.Order)
                .filter(models.Order.client_id == user_id,
                        models.Order.id == order_id)
                .first()
                )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The order with ID {order_id} was not found.'
            )

        if order.status:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to cancel this order. It has already been approved."
            )

        self.session.delete(order)
        self.session.commit()
    
    def change_status(self, order_id: int, user_id:int, situation: bool):
        order = (self.session.query(models.Order)
                .join(models.Product,
                      models.Product.id == models.Order.product_id)
                .filter(models.Product.user_id == user_id,
                        models.Order.id == order_id)
                .first()
                 )
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The order with ID {order_id} was not found.'
            )
        
        order.status = situation
        self.session.commit()

    def search_vendor_order(self, order_id: int, user_id: int):
        order = (self.session.query(models.Order)
                .join(models.Product,
                      models.Product.id == models.Order.product_id)
                .filter(models.Product.user_id == user_id,
                        models.Order.id == order_id)
                .first()
                 )
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The order with ID {order_id} was not found.'
            )
        
        return OrderResponse.model_validate(order)