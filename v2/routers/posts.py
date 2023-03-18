import os
import datetime
import shutil
from fastapi import APIRouter, HTTPException, Depends, Request, status, FastAPI, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict
import jwt_manager
import schemas, models
from database_manager import get_db
import schemas.posts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter(tags=['posts'])
template = Jinja2Templates(directory='templates')


@router.get('/')
def home_page(request: Request,
              db: Session = Depends(get_db),
              current_user: models.auth.User | None = Depends(jwt_manager.get_current_user)):
    last_post = db.query(models.posts.Post).order_by(desc(models.posts.Post.last_update)).limit(10)
    context = {'request': request, 'posts': last_post, 'user': current_user}
    return template.TemplateResponse('home.html', context)


@router.get('/post')
def create_post(request: Request, current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    """get create post form"""

    context = {'request': request, 'user': current_user}
    return template.TemplateResponse('create_post.html', context)


# @router.post('/post', response_model=schemas.posts.ResponsePost | None, status_code=status.HTTP_201_CREATED)
# def create_post(payload: schemas.posts.CreatePost,
#                 db: Session = Depends(get_db),
#                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
#                 ):
#     """create new post depends on login user"""
#     print(payload)
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you must be login')
#
#     payload_dict = payload.dict()
#
#     if current_user.role == "admin":
#         payload_dict.update({'status': 'published', 'user_id': current_user.user_id})
#     elif current_user.role == "writer":
#         payload_dict.update({'status': 'pending', 'user_id': current_user.user_id})
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')

    # new_post = models.posts.Post(**payload_dict)
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    # return new_post


import shutil
@router.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(request: Request,
                      post_title: str = Form(...),
                      post_content: str = Form(...),
                      post_image: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                      ):
    image_url = f'/statics/images/upload/post/{post_image.filename}'
    with open(f'{BASE_DIR}{image_url}', "wb") as buffer:
        shutil.copyfileobj(post_image.file, buffer)

    payload_dict = {}
    if current_user.role == "admin":
        payload_dict.update({'status': 'published', 'user_id': current_user.user_id})
    elif current_user.role == "writer":
        payload_dict.update({'status': 'pending', 'user_id': current_user.user_id})
    else:
        context = {'request': request, 'user': current_user, 'status': status.HTTP_403_FORBIDDEN}
        return template.TemplateResponse('create_post.html', context)

    try:
        new_post = models.posts.Post(**payload_dict, title=post_title, content=post_content, image=image_url)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        context = {'request': request, 'user': current_user, 'status': status.HTTP_201_CREATED}
        return template.TemplateResponse('create_post.html', context)
    except Exception:
        context = {'request': request, 'user': current_user, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}
        return template.TemplateResponse('create_post.html', context)


@router.get("/posts/{id}", response_model=Dict)
def get_post(request: Request, id: int,
             db: Session = Depends(get_db),
             current_user: Session = Depends(jwt_manager.get_current_user)
             ):

    post = db.query(models.posts.Post).filter(models.posts.Post.post_id == id).first()

    if not post:
        return template.TemplateResponse('404.html', {'request': request})

    comments = db.query(models.posts.Comment) \
        .filter(models.posts.Comment.post_id == post.post_id) \
        .order_by(desc(models.posts.Comment.publish_date)).all()

    context = {'request': request, 'post': post, 'comments': comments, 'user': current_user}
    return template.TemplateResponse('post.html', context)


@router.get("/all_posts", response_model=List[schemas.posts.GetPost])
def all_published_post(request: Request,
                       db: Session = Depends(get_db),
                       current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                       ):

    all_posts = db.query(models.posts.Post).filter(models.posts.Post.status == "published").all()
    context = {'request': request, 'all_posts': all_posts, 'user': current_user}
    return template.TemplateResponse('posts.html', context)


@router.get("/admin/posts/{post_status}", response_model=List[schemas.posts.GetPost])
def get_post_by_status(request: Request, post_status: str, db: Session = Depends(get_db),
                       current_user: models.auth.User = Depends(jwt_manager.get_current_user)):

    """get all post by status (published, pending, draft, reject) => only for admin user"""
    if current_user and current_user.role == 'admin':
        all_posts = db.query(models.posts.Post).filter(models.posts.Post.status == post_status).all()
        # context = {'request': request, 'all_posts': all_posts}
        # return template.TemplateResponse('home.html', context)
        return all_posts
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')


@router.get("/users/{user_name}", response_model=List[schemas.posts.GetPost], name='user_post')
def user_post(request: Request, user_name: str, db: Session = Depends(get_db)):

    user = db.query(models.auth.User).filter(models.auth.User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {user_name} not found')

    all_user_posts = db.query(models.posts.Post).filter(models.posts.Post.user_id == user.user_id)
    context = {'request': request, 'all_user_posts': all_user_posts}
    return template.TemplateResponse('user_post.html', context)


@router.post('/comment', response_model=schemas.posts.ResponseComment, status_code=status.HTTP_201_CREATED)
def create_comment(payload: schemas.posts.CommentBase,
                   db: Session = Depends(get_db),
                   current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                   ):

    """create new comment for specific post depends on login user"""

    payload_dict = payload.dict()
    payload_dict.update({'status': 'pending', 'user_id': current_user.user_id})
    new_comment = models.posts.Comment(**payload_dict)
    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception:
        return {'detail': 'error'}

@router.get('/comments', response_model=List[schemas.posts.ResponseComment])
def get_all_comment(request: Request, db: Session = Depends(get_db)):
    all_comments = db.query(models.posts.Comment).all()
    return all_comments


@router.get('/comments/{user_name}', response_model=List[schemas.posts.ResponseComment])
def get_all_comment_user(request: Request,
                         user_name: str,
                         db: Session = Depends(get_db)):

    user = db.query(models.auth.User).filter(models.auth.User.username == user_name).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_name} not found")

    all_comment = db.query(models.posts.Comment).filter(models.posts.Comment.user_id == user.user_id).all()

    context = {'request': request, 'comments': all_comment, 'user': user}
    return template.TemplateResponse('users_comments.html', context)


@router.delete('/posts/delete/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):
    post_query = db.query(models.posts.Post).filter(models.posts.Post.post_id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    else:
        if post.user_id == current_user.user_id or current_user.role == 'admin':
            post_query.delete(synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'your not owner of this post')

@router.get('/post/update/{post_id}')
def update_post(request: Request,
                post_id: int,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):
    post = db.query(models.posts.Post).filter(models.posts.Post.post_id == post_id).first()

    if not post:
        return template.TemplateResponse('404.html', {'request': request})

    if not post.user_id == current_user.user_id:
        return template.TemplateResponse('404.html', {'request': request})

    context = {'request': request, 'post': post, 'user': current_user}
    return template.TemplateResponse('update_post.html', context)


@router.put('/post/update/{post_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(post_id: int,
                payload: schemas.posts.updatePost,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):

    post_query = db.query(models.posts.Post).filter(models.posts.Post.post_id == post_id)
    post = post_query.first()

    if post is not None and post.user_id == current_user.user_id:
        payload_dict = payload.dict()
        payload_dict.update({"last_update": datetime.datetime.now()})
        post_query.update(payload_dict, synchronize_session=False)
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@router.get('/dashboard/comment/manage')
def get_comment_manage():
    pass


@router.get('/dashboard/post/manage')
def get_post_manage():
    pass
