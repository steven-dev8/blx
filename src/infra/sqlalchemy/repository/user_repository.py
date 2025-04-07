from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schema.schemas import UserResponse, UserEdit, UserProduct, UserCreate, OrderUserSearch, UserLogin
from src.infra.sqlalchemy.models import models
from src.infra.validators.user_validators import *
from src.infra.providers import hash_provider
from sqlalchemy.exc import IntegrityError
from src.infra.providers import hash_provider


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
            user.password = hash_provider.generate_hash(user.password)
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

        return UserResponse.model_validate(add_user)

    def to_list(self):
        user_list = self.session.query(models.User.id, models.User.name, models.User.number).all()
        if not user_list:
            raise HTTPException(
                                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Temporarily unavailable. Fix in progress."
                                )
        
        format_user = [UserResponse.model_validate(user) for user in user_list]
        return format_user

    def query_user(self, id_user: int):
        result_user = (
            self.session.query(
                models.User
            )
            .filter(models.User.id == id_user)
            .first()
        )

        if not result_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {id_user} doesn't exist."
            )

        return UserResponse.model_validate(result_user)

    def delete_user(self, id_user: int):
        query = self.session.query(models.User).filter(models.User.id == id_user).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {id_user} was not found."
                )

        self.session.delete(query)
        self.session.commit()
    
        return None

    def user_product(self, id_user: int):
        products_query = self.session.query(models.Product).filter(models.Product.user_id == id_user).all()
        user_query = self.session.query(models.User.id, models.User.name).filter(models.User.id == id_user).first()

        if not user_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {id_user} was not found."
                )

        formatted_response = UserProduct(
                                        id=user_query[0],
                                        name=user_query[1],
                                        products=products_query
                                        )
        return formatted_response

    def user_order(self, id_user: int):
        order_query = self.session.query(models.Order).join(
                                                            models.Product,
                                                            models.Product.id == models.Order.product_id
                                                            ).filter(models.Product.user_id == id_user).all()
        
        if not order_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Orders not fould"
            )

        return [OrderUserSearch.model_validate(order) for order in order_query]

    def edit_user(self, id_user: int, user: UserEdit):
        user_query = self.session.query(models.User).filter(models.User.id == id_user).first()

        if not user_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user with ID {id_user} was not found."
                )
        
        if not validate_create(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The provided user data is invalid. Please check the input fields."
            )

        user_query.name = user.name
        user_query.login = user.login
        user_query.number = user.number
        user_query.password = user.password
        self.session.commit()
        return None
    
    def login_token(self, user: UserLogin):
        login = user.login
        password = user.password
        query = self.session.query(models.User).filter(
                                                       models.User.login == login
                                                       ).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user found with that login"
                )

        verify_password = hash_provider.verify_hash(password, query.password)

        if not verify_password:
            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password is incorrect"
                                ) 
        
        # JWT WILL BE ADDED