from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from typing import Dict

import models.auth
import schemas.auth
from database_manager import get_db


ALGORITHM = "HS256"
TOKEN_PERIOD_MINUTES = 30
SECRET_KEY = "d3b36f16f463a2dc91dfe6d3e3a4d7c8d1ae7776d55aad6a725626cdc0277e3f"


def create_jwt_token(data: Dict):
    encode_data = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=TOKEN_PERIOD_MINUTES)
    encode_data.update({'exp': exp})

    jwt_token = jwt.encode(encode_data, SECRET_KEY, ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_id = token_decode.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.auth.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl='login')), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='credentials fail',
                                          headers={"WWW.Authenticate": "Bearer"}
                                          )

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.auth.User).filter(models.auth.User.user_id == token.user_id).first()
    return user
