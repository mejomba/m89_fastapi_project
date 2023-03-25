from fastapi import status, HTTPException, Request, Depends, APIRouter, Cookie, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from psycopg2.errors import UniqueViolation
import jwt_manager
import models.auth
import models.posts
import schemas.auth
from database_manager import get_db
import utils
from datetime import datetime
import settings


router = APIRouter(tags=['auth'])
template = Jinja2Templates('templates')


@router.get('/base')
def get_base(request: Request,
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
             ):

    context = {'request': request, 'user': current_user}
    return template.TemplateResponse('base.html', context)


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.auth.ResponseUser | None)
def create_user(payload: schemas.auth.CreateUser, db: Session = Depends(get_db)):

    payload.password = utils.hash_password(payload.password)

    payload_dict = payload.dict()
    payload_dict.update({"role": "regular_user", 'image': '/statics/images/upload/user/no_image.png'})
    new_user = models.auth.User(**payload_dict)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user already exist')


@router.get('/user/update/{user_id}')
def update_user(request: Request,
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    context = {'request': request, 'user': current_user}

    return template.TemplateResponse('update_user.html', context)


@router.put('/user/update/{user_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_user(request: Request,
                response: Response,
                user_id: int,
                payload: schemas.auth.UpdateUser,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    context = {'request': request, 'user': current_user}

    user_query = db.query(models.auth.User).filter(models.auth.User.user_id == user_id)
    user = user_query.first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    if payload.remove_image:
        image_url = f'/statics/images/upload/user/no_image.png'
    elif image := payload.image:
        try:
            image_url = utils.save_image(image)
        except Exception:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return
    elif not payload.image and not payload.remove_image:
        image_url = user.image
    else:
        image_url = f'/statics/images/upload/user/no_image.png'

    payload_dict = payload.dict()
    payload_dict.pop('remove_image')
    payload_dict.update({'image': image_url, 'last_update': datetime.now()})

    try:
        user_query.update(payload_dict, synchronize_session=False)
        db.commit()
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return




@router.post('/login', response_model=schemas.auth.Token)
def user_login(response: Response, user_credentials: schemas.auth.UserLogin, db: Session = Depends(get_db)):
    user_query = db.query(models.auth.User).filter(models.auth.User.email == user_credentials.email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    try:
        token = jwt_manager.create_jwt_token({"user_id": user.user_id})
        response.set_cookie('access_token', str(token))
        user_query.update({'is_authenticated': True}, synchronize_session=False)
        db.commit()
        return {"access_token": token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")


@router.get('/logout')
async def user_logout(request: Request, response: Response,
                      db: Session = Depends(get_db),
                      current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                      ):

    response.delete_cookie('access_token')

    try:
        user_query = db.query(models.auth.User).filter(models.auth.User.user_id == current_user.user_id)
        user_query.update({'is_authenticated': False}, synchronize_session=False)
        db.commit()
        return RedirectResponse(request.url_for('home_page'), headers=response.headers)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='error')


@router.get('/dashboard')
def user_profile(request: Request,
                 db: Session = Depends(get_db),
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                 ):
    if current_user:
        user_posts = db.query(models.posts.Post)\
            .filter(models.posts.Post.user_id == current_user.user_id)\
            .order_by(desc(models.posts.Post.publish_date)).all()

        comments = db.query(models.posts.Comment).filter(models.posts.Comment.user_id == current_user.user_id).all()
        context = {'request': request, "user": current_user, "user_posts": user_posts, 'comments': comments}
        return template.TemplateResponse('dashboard.html', context=context)
    else:
        context = {'request': request, "user": current_user}
        return template.TemplateResponse('dashboard.html', context)


@router.post('/dashboard/request/writer', status_code=status.HTTP_201_CREATED)
def request_change_role(request: Request,
                        db: Session = Depends(get_db),
                        current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                        ):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='برای دسترسی به این بخش باید وارد شوید')
    payload = {'user_id': current_user.user_id, 'request_name': 'writer', 'status': 'pending'}
    user_request = models.auth.UserRequest(**payload)
    try:
        db.add(user_request)
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='خطا در درخواست، احتمالا قبلا این درخواست ارسال شده')


@router.get('/dashboard/user/manage')
def get_user_manage(request: Request,
                    db: Session = Depends(get_db),
                    current_user: models.auth.User = Depends(jwt_manager.get_current_user)):

    if current_user.role == 'admin':
        user_requests = db.query(models.auth.UserRequest).order_by(models.auth.UserRequest.status).all()
        c = 0
        for item in user_requests:
            if item.status == 'pending':
                c += 1
        # user_requests_pending = db.query(models.auth.UserRequest).filter(models.auth.UserRequest.status == 'pending').all()
        context = {'request': request, 'user': current_user, 'user_requests': user_requests, 'request_count': c}
        return template.TemplateResponse('user_manage.html', context)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='شما به این بخش دسترسی ندارید')


@router.post('/dashboard/user/manage/{user_request_id}', status_code=status.HTTP_200_OK)
def change_user_role(
                     user_request_id: int,
                     payload: schemas.auth.ChangeUserRole,
                     db: Session = Depends(get_db),
                     current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                     ):

    if current_user.role == 'admin':
        if payload.user_request_action == 'ok':
            user_request_query = db.query(models.auth.UserRequest).filter(models.auth.UserRequest.user_request_id == user_request_id)
            user_request_query.update({'status': 'published', 'last_update': datetime.now()}, synchronize_session=False)
            db.commit()

            user_request = user_request_query.first()
            user_query = db.query(models.auth.User).filter(models.auth.User.user_id == user_request.user_id)
            user_query.update({'role': 'writer'}, synchronize_session=False)
            db.commit()
        elif payload.user_request_action == 'reject':
            user_request_query = db.query(models.auth.UserRequest).filter(
                models.auth.UserRequest.user_request_id == user_request_id)
            user_request_query.update({'status': 'reject', 'last_update': datetime.now()}, synchronize_session=False)
            db.commit()

    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='شما به این بخش دسترسی ندارید')


@router.delete('/users_manage/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(request: Request,
                response: Response,
                user_id: int,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):
    user_query = db.query(models.auth.User).filter(models.auth.User.user_id == user_id)
    user = user_query.first()

    context = {'request': request, 'user': current_user}

    if user is None:
        return template.TemplateResponse('404.html', context)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    else:
        if user.user_id == current_user.user_id or current_user.role == 'admin':
            user_query.delete(synchronize_session=False)
            db.commit()
            RedirectResponse.delete_cookie(response, key='access_token')
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'you are not admin')