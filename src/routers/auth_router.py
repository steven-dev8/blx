from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.repository.user_repository import ProcessUser
from src.schema.schemas import UserResponse, UserCreate, UserLogin
from src.infra.sqlalchemy.config.database import get_db
from typing import List, Union


router = APIRouter()

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup_user(user: UserCreate, session: Session = Depends(get_db)):
    user_db = ProcessUser(session).create(user)
    return user_db


@router.post('/token')
def sigin_user(user: UserLogin, session: Session = Depends(get_db)):
    token = ProcessUser(session).login_token(user)
    return token