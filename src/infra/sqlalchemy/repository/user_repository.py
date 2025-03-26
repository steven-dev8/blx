from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from src.schema.schemas import UserResponse, UserEdit, UserProduct, UserBase, UserCreate
from src.infra.sqlalchemy.models import models
from src.infra.validators.user_validators import *
from sqlalchemy.exc import IntegrityError

class ProcessUser:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user: UserCreate):
        if not validate_create(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="The provided user data is invalid. Please check the input fields."
                )
        try:
            add_user = models.User(
                                name=user.name,
                                login=user.login,
                                password=user.password,
                                number=user.number
                                )
            self.session.add(add_user)
            self.session.commit()
            self.session.refresh(add_user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Login '{user.login}' already exists."
                )

        return UserResponse(id=add_user.id, name=add_user.name, number=add_user.number)
        

    def to_list(self):
        user_list = self.session.query(models.User.id, models.User.name, models.User.number).all()
        if user_list:
            format_user = [UserResponse(id=id_u, name=name_u, number=number_u) for id_u, name_u, number_u in user_list]
            return format_user
        return user_list

    def query_user(self, id_user: int):
        result_user = self.session.query(models.User.id, models.User.name, models.User.number).filter(
            models.User.id == id_user
        ).first()
        if result_user:
            user = UserResponse(id=result_user[0], name=result_user[1], number=result_user[2])
            return user
        return result_user
    
    def delete_user(self, id_user: int):
        query = self.session.query(models.User).filter(models.User.id == id_user).first()
        if query:
            self.session.delete(query)
            self.session.commit()
            return {"message": f"The user {query.id} has been deleted"}
        return query

    def user_product(self, id_user: int):
        prd_query = self.session.query(models.Product).filter(models.Product.user_id == id_user).all()
        user_query = self.session.query(models.User.id, models.User.name).filter(models.User.id == id_user).first()
        print(prd_query, user_query)
        if user_query:
            formate = UserProduct(id=user_query[0], name=user_query[1], products=prd_query)
            return formate
        return None

    def edit_user(self, id_user: int, user: UserEdit):
        user_query = self.session.query(models.User).filter(models.User.id == id_user).first()
        if user_query:
            user_query.name = user.name
            user_query.number = user.number
            user_query.password = user.password
            self.session.commit()
            self.session.refresh(user_query)
            return UserResponse(id=user_query.id, name=user_query.name, number=user_query.number)
        return user_query
        