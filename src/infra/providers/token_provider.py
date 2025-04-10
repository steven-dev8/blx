from datetime import datetime, timedelta, timezone
import jwt


SECRET_KEY = "SECRET_KEY_HERE"
ALGORITHM = "HS256"
EXPIRES_IN_MINUTE = 300



def create_access_token(data: dict):
    content_data = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_IN_MINUTE)

    content_data.update({'exp': expiration})

    token_jwt = jwt.encode(content_data, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def validate_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    login = payload.get('sub')
    return login