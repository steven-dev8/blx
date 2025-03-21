from sqlalchemy.orm import Session
from src.schema.schemas import Product
from src.infra.sqlalchemy.models import models


class ProcessProduct:
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(self, product: Product):
        db_product = models.Product(id=product.id,
                                    name=product.name,
                                    description=product.description,
                                    price=product.price,
                                    avaliable=product.avaliable)
        
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    
    def to_list(self):
        products = self.db.query(models.Product).all()
        return products 