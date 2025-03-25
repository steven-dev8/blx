from sqlalchemy.orm import Session
from src.schema.schemas import Product, ProductEdit
from src.infra.sqlalchemy.models import models


class ProcessProduct:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, product: Product):
        db_product = models.Product(name=product.name,
                                    description=product.description,
                                    price=product.price,
                                    avaliable=product.avaliable,
                                    user_id=product.user_id)
        
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product
     
    def to_list(self):
        products = self.session.query(models.Product).all()
        return products 

    def search(self, id_query):
        result = self.session.query(models.Product).filter(models.Product.id == id_query).first()
        return result

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
            query.avaliable = product.avaliable
            self.session.commit()
            self.session.refresh(query)
            return ProductEdit(name=query.name,
                               description=query.description,
                               price=query.price,
                               avaliable=query.avaliable)