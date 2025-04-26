from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from src.infra.sqlalchemy.repository.user_repository import ProcessUser
from jwt.exceptions import PyJWTError


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def get_registered_user(token: str = Depends(oauth2_schema),
                        session: Session = Depends(get_db)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
            )
    
    try:
        login = token_provider.validate_access_token(token)
    except PyJWTError:
        raise exception
    
    if not login:
        raise exception
    
    user = ProcessUser(session).search_user_login(login)

    if not user:
        raise exception

    return user