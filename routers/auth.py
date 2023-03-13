from fastapi import status, HTTPException, Request, Depends, APIRouter, Cookie, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from psycopg2.errors import UniqueViolation
import jwt_manager
import models.auth
import models.posts
import schemas.auth
from database_manager import get_db
import utils


router = APIRouter(tags=['auth'])

template = Jinja2Templates('templates')


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.auth.ResponseUser | None)
def create_user(payload: schemas.auth.CreateUser, db: Session = Depends(get_db)):

    payload.password = utils.hash_password(payload.password)

    payload_dict = payload.dict()
    payload_dict.update({"role": "regular_user"})
    new_user = models.auth.User(**payload_dict)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user already exist')


@router.post('/login', response_model=schemas.auth.Token)
def user_login(response: Response, user_credentials: schemas.auth.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.auth.User).filter(models.auth.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    token = jwt_manager.create_jwt_token({"user_id": user.user_id})
    response.set_cookie('access_token', str(token))
    return {"access_token": token, "token_type": "bearer"}


@router.get('/dashboard')
def user_profile(request: Request,
                 db: Session = Depends(get_db),
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                 ):
    user_posts = db.query(models.posts.Post).filter(models.posts.Post.user_id == current_user.user_id).all()
    comments = db.query(models.posts.Comment).filter(models.posts.Comment.user_id == current_user.user_id).all()
    context = {'request': request, "user": current_user, "user_posts": user_posts, 'comments': comments}
    return template.TemplateResponse('dashboard.html', context=context)


@router.get('/logout')
def user_logout(request: Request, response: Response,
                 db: Session = Depends(get_db),
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                 ):
    response.delete_cookie('access_token')
    context = {'request': request}
    return template.TemplateResponse('home.html', context=context)