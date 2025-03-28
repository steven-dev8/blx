from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models import models
from src.schema.schemas import OrderBase, OrderCreate, OrderResponse
import src.infra.validators.order_validators as validator

class ProcessOrder:
    def __init__(self, session: Session):
        self.session = session
    

    def create_order(self, order: OrderCreate):
        user = self.session.query(models.User.id).filter(models.User.id == order.client_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {order.client_id} was not found."
                )
        
        product = self.session.query(models.Product.quantity).filter(models.Product.id == order.product_id).scalar()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with ID {order.product_id} was not found."
            )
        print(order.dict())
        validator.additional_check(order, product)
        new_order = models.Order(**order.dict())
        
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
        
        return OrderResponse.model_validate(result)

    def search_order(self):
        ...
    
    def delete_order(self):
        ...
    
    def change_status(self):
        ...