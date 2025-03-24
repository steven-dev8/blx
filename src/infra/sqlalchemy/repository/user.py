from sqlalchemy.orm import Session
from typing import List
from src.schema.schemas import User, UserResponse, UserProduct
from src.infra.sqlalchemy.models import models

class ProcessUser:
    def __init__(self, db: Session):
        self.db = db
    

    def create(self, user: User):
        add_user = models.User(id=user.id,
                               name=user.name,
                               password=user.password,
                               number=user.number)
        
        self.db.add(add_user)
        self.db.commit()
        self.db.refresh(add_user)
        return add_user
    

    def to_list(self):
        user_list = self.db.query(models.User.id, models.User.name, models.User.number).all()
        format_user = [UserResponse(id=id_u, name=name_u, number=number_u) for id_u, name_u, number_u in user_list]
        return format_user
    

    def query_user(self, id_user: int):
        result_user = self.db.query(models.User.id, models.User.name, models.User.number).filter(
            models.User.id == id_user
        ).first()
        user = UserResponse(id=result_user[0], name=result_user[1], number=result_user[2])
        return user
    

    def delete_user(self, id_user: int):
        query = self.db.query(models.User).filter(models.User.id == id_user).first()
        if query:
            self.db.delete(query)
            self.db.commit()
            return {"message": f"The user {query.id} has been deleted"}
        return False
    

    def user_product(self, id_user: int):
        prd_query = self.db.query(models.Product).filter(models.Product.user_id == id_user).all()
        user_query = self.db.query(models.User.id, models.User.name).filter(models.User.id == id_user).first()
        formate = UserProduct(id=user_query[0], name=user_query[1], products=prd_query)
        return formate