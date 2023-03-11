from fastapi import status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session

import jwt_manager
import models.auth
import schemas.auth
from database_manager import get_db
import utils
from main import template

router = APIRouter(tags=['auth'])


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.auth.ResponseUser)
def create_user(payload: schemas.auth.CreateUser, db: Session = Depends(get_db)):

    payload.password = utils.hash_password(payload.password)

    payload_dict = payload.dict()
    payload_dict.update({"role": "regular_user"})
    new_user = models.auth.User(**payload_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login', response_model=schemas.auth.Token)
def user_login(user_credentials: schemas.auth.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.auth.User).filter(models.auth.User.email == user_credentials.email).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    token = jwt_manager.create_jwt_token({"user_id": user.user_id})
    return {"access_token": token, "token_type": "bearer"}


@router.get('/dashboard')
def user_profile(request: Request, current_user: models.auth.User = Depends(jwt_manager.get_current_user()),
                 db: Session = Depends(get_db)
                 ):

    context = {'request': request, "user": current_user}
    return template.TemplateResponse('dashboard.html', context=context)
