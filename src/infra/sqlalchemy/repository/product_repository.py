from sqlalchemy.orm import Session
from src.schema.schemas import ProductBase, ProductCreate, ProductEdit, ProductResponse
from src.infra.sqlalchemy.models import models


class ProcessProduct:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, product: ProductCreate):
        db_product = models.Product(
                                    name=product.name,
                                    user_id=product.user_id,
                                    description=product.description,
                                    price=product.price,
                                    quantity=product.quantity,
                                    )
        
        if db_product.quantity > 0:
            db_product.avaliable=True

        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product
     
    def to_list(self):
        products = self.session.query(models.Product).all()
        return products 

    def search(self, id_query: int):
        result = self.session.query(models.Product).filter(models.Product.id == id_query).first()
        return ProductResponse(
                            id=result.id,
                            user_id=result.user_id,
                            name=result.name,
                            description=result.description,
                            price=result.price,
                            quantity=result.quantity,
                            avaliable=result.avaliable
                            
        )

    def delete_product(self, id_prd: int):
        query = self.session.query(models.Product).filter(models.Product.id == id_prd).first()
        if query:
            self.session.delete(query)
            self.session.commit()
            return f'The product {query.name} has been deleted'
        return False
    
    def edit_product(self, id_user: int, product: ProductEdit):
        query = self.session.query(models.Product).filter(models.Product.id == id_user).first()
        if query:
            query.name = product.name
            query.description = product.description
            query.price = product.price
            query.quantity = product.quantity
            if product.quantity > 0:
                query.avaliable = True
            self.session.commit()
            self.session.refresh(query)
            return ProductResponse(
                            id=result.id,
                            user_id=result.user_id,
                            name=result.name,
                            description=result.description,
                            price=result.price,
                            quantity=result.quantity,
                            avaliable=result.avaliable        
        )