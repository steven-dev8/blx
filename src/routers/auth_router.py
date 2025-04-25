from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.user_repository import ProcessUser
from src.schema.schemas import UserResponse, UserCreate, UserLogin, UserLoginOut
from src.infra.sqlalchemy.config.database import get_db
from src.routers.auth_utils import get_registered_user


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Authentication"])
def signup_user(user: UserCreate, session: Session = Depends(get_db)):
    user_db = ProcessUser(session).create(user)
    return user_db


@router.post('/token', tags=["Authentication"])
def signin_user(user: UserLogin, session: Session = Depends(get_db)):
    token = ProcessUser(session).login_token(user)
    return token


@router.get('/me', response_model=UserLoginOut, tags=["Authentication"])
def me(user: UserLoginOut = Depends(get_registered_user)):
    return user
