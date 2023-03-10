from fastapi import status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session

import models.auth
import schemas.auth
from database_manager import get_db
import utils


router = APIRouter(tags=['auth'])


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.auth.ResponseUser)
def create_user(user: schemas.auth.CreateUser, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)
    new_user = models.auth.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
