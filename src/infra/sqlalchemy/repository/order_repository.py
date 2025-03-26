from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models import models
from src.schema.schemas import OrderBase, OrderCreate, OrderResponse

class ProcessOrder:
    def __init__(self, session: Session):
        self.session = session
    

    def create_order(self, order: OrderCreate):
        new_order = models.Order(client_id=order.client_id,
                                 product_id=order.product_id,
                                 quantity=order.quantity,
                                 status=order.status,
                                 address=order.address,
                                 observation=order.obs)
        
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        return OrderResponse(
                            id=new_order.id,
                            client_id=new_order.client_id,
                            product_id=new_order.product_id,
                            quantity=new_order.quantity,
                            status=new_order.status,
                            address=new_order.address,
                            observation=new_order.observation
                             )