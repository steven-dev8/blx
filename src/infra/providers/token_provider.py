from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pathlib import Path
import jwt
import os

dotenv_path = Path('.') / '.env'
load_dotenv(dotenv_path=dotenv_path)


SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRES_IN_MINUTE = int(os.getenv("EXPIRES_IN_MINUTE", "15"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

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