import os
import datetime
import base64
import shutil
import time
import re
from fastapi import APIRouter, HTTPException, Depends, Request, status, FastAPI, UploadFile, File, Form, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict, Optional
import jwt_manager
import schemas, models
from database_manager import get_db
import schemas.posts
import jalali_date
from settings import BASE_DIR
from utils import save_image


router = APIRouter(tags=['posts'])
template = Jinja2Templates(directory='templates')


@router.get('/')
def home_page(request: Request,
              db: Session = Depends(get_db),
              current_user: models.auth.User | None = Depends(jwt_manager.get_current_user)):
    last_post = db.query(models.posts.Post).filter(models.posts.Post.status == 'published').order_by(desc(models.posts.Post.last_update)).limit(10)
    context = {'request': request, 'posts': last_post, 'user': current_user}
    return template.TemplateResponse('home.html', context)


@router.get('/post')
def create_post(request: Request, current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    """get create post form"""

    context = {'request': request, 'user': current_user}
    return template.TemplateResponse('create_post.html', context)


@router.post('/post', response_model=schemas.posts.ResponsePost | None, status_code=status.HTTP_201_CREATED)
def create_post(request: Request,
                response: Response,
                payload: schemas.posts.CreatePost,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):

    """create new post depends on login user"""

    context = {'request': request, 'user': current_user}

    if not current_user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return template.TemplateResponse('create_post.html', context)

    payload_dict = payload.dict()
    if image := payload.image:
        try:
            image_url = save_image(image)
        except Exception:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return
    else:
        image_url = f'/statics/images/upload/post/no_image.png'

    if current_user.role == "admin":
        payload_dict.update({'status': 'published', 'user_id': current_user.user_id, 'image': image_url})
    elif current_user.role == "writer":
        payload_dict.update({'status': 'pending', 'user_id': current_user.user_id, 'image': image_url})
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    try:
        new_post = models.posts.Post(**payload_dict)
        db.add(new_post)
        db.commit()
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# import shutil
# @router.post("/post", status_code=status.HTTP_201_CREATED)
# async def create_post(request: Request,
#                       post_title: str = Form(...),
#                       post_content: str = Form(...),
#                       post_image: UploadFile = File(...),
#                       db: Session = Depends(get_db),
#                       current_user: models.auth.User = Depends(jwt_manager.get_current_user)
#                       ):
#     image_url = f'/statics/images/upload/post/{post_image.filename}'
#     with open(f'{BASE_DIR}{image_url}', "wb") as buffer:
#         shutil.copyfileobj(post_image.file, buffer)
#
#     payload_dict = {}
#     if current_user.role == "admin":
#         payload_dict.update({'status': 'published', 'user_id': current_user.user_id})
#     elif current_user.role == "writer":
#         payload_dict.update({'status': 'pending', 'user_id': current_user.user_id})
#     else:
#         context = {'request': request, 'user': current_user, 'status': status.HTTP_403_FORBIDDEN}
#         return template.TemplateResponse('create_post.html', context)
#
#     try:
#         new_post = models.posts.Post(**payload_dict, title=post_title, content=post_content, image=image_url)
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#         context = {'request': request, 'user': current_user, 'status': status.HTTP_201_CREATED}
#         return template.TemplateResponse('create_post.html', context)
#     except Exception:
#         context = {'request': request, 'user': current_user, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}
#         return template.TemplateResponse('create_post.html', context)


@router.get("/posts/{id}", response_model=Dict)
def get_post(request: Request, id: int,
             db: Session = Depends(get_db),
             current_user: Session = Depends(jwt_manager.get_current_user)
             ):

    post = db.query(models.posts.Post).filter(models.posts.Post.post_id == id).first()

    if not post:
        return template.TemplateResponse('404.html', {'request': request, 'user': current_user})

    comments = db.query(models.posts.Comment) \
        .filter(models.posts.Comment.post_id == post.post_id).filter(models.posts.Comment.status == 'published') \
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
def get_post_by_status(request: Request,
                       post_status: str,
                       db: Session = Depends(get_db),
                       current_user: models.auth.User = Depends(jwt_manager.get_current_user)):

    """get all post by status (published, pending, draft, reject) => only for admin user"""

    if current_user and current_user.role == 'admin':
        if post_status == 'all':
            all_posts = db.query(models.posts.Post).all()
        else:
            all_posts = db.query(models.posts.Post).filter(models.posts.Post.status == post_status).all()

        context = {'request': request, 'user': current_user, 'posts': all_posts}
        return template.TemplateResponse('post_manage.html', context)
        # return all_posts
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')


@router.get("/users/{user_name}", response_model=List[schemas.posts.GetPost], name='user_post')
def user_post(request: Request, user_name: str, db: Session = Depends(get_db)):

    user = db.query(models.auth.User).filter(models.auth.User.username == user_name).first()
    if user is None:
        return template.TemplateResponse('404.html', context={'request': request})
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {user_name} not found')

    all_user_posts = db.query(models.posts.Post).filter(models.posts.Post.user_id == user.user_id).filter(models.posts.Post.status=='published').all()
    context = {'request': request, 'user': user, 'all_user_posts': all_user_posts}
    return template.TemplateResponse('user_post.html', context)


@router.post('/comment', response_model=schemas.posts.ResponseComment, status_code=status.HTTP_201_CREATED)
def create_comment(payload: schemas.posts.CommentBase,
                   db: Session = Depends(get_db),
                   current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                   ):

    """create new comment for specific post depends on login user"""

    payload_dict = payload.dict()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')

    if current_user.role == 'admin':
        payload_dict.update({'status': 'published', 'user_id': current_user.user_id})
    else:
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
                         db: Session = Depends(get_db),
                         current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                         ):
    if not current_user:
        return template.TemplateResponse('404.html', {'request': request})
    # user = db.query(models.auth.User).filter(models.auth.User.username == user_name).first()

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_name} not found")

    # all_comment = db.query(models.posts.Comment).filter(models.posts.Comment.user_id == user.user_id).all()
    all_comment = db.query(models.posts.Comment).filter(models.posts.Comment.user_id == current_user.user_id).all()

    context = {'request': request, 'comments': all_comment, 'user': current_user}
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

    if current_user.role == 'admin' or post.user_id == current_user.user_id:
        context = {'request': request, 'post': post, 'user': current_user}
        return template.TemplateResponse('update_post.html', context)

    return template.TemplateResponse('404.html', {'request': request})



@router.put('/post/update/{post_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(response: Response,
                post_id: int,
                payload: schemas.posts.UpdatePost,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):

    post_query = db.query(models.posts.Post).filter(models.posts.Post.post_id == post_id)
    post = post_query.first()

    if post and (post.user_id == current_user.user_id or current_user.role == 'admin'):
        if payload.remove_image:
            image_url = f'/statics/images/upload/post/no_image.png'
        elif image := payload.image:
            try:
                image_url = save_image(image)
            except Exception:
                response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                return
        elif not payload.image and not payload.remove_image:
            image_url = post.image
        else:
            image_url = f'/statics/images/upload/post/no_image.png'

        payload_dict = payload.dict()
        payload_dict.pop('remove_image')

        if current_user.role == "admin":
            payload_dict.update({'status': 'published', 'user_id': post.user_id, 'image': image_url})
        elif current_user.role == "writer":
            payload_dict.update({'status': 'pending', 'user_id': post.user_id, 'image': image_url})
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return

        try:
            post_query.update(payload_dict, synchronize_session=False)
            db.commit()
        except Exception:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@router.get('/dashboard/comment/manage')
def comment_manage(request: Request,
                   db: Session = Depends(get_db),
                   current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    if current_user.role == 'admin':
        comments = db.query(models.posts.Comment).order_by(models.posts.Comment.status).all()
        context = {'request': request, 'comments': comments, 'user': current_user}
        return template.TemplateResponse('comment_manage.html', context)


@router.post('/dashboard/comment/manage/{comment_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def comment_manage(request: Request,
                   response: Response,
                   comment_id: int,
                   payload: schemas.posts.UserCommentAction,
                   db: Session = Depends(get_db),
                   current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                   ):

    comment_query = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id)
    comment = comment_query.first()

    context = {'request': request, 'user': current_user}

    if current_user.role == 'admin':

        if not comment:
            return template.TemplateResponse('404.html', context)
        if payload.user_action == 'ok':
            comment_query.update({'status': 'published', 'last_update': datetime.datetime.now()}, synchronize_session=False)
            db.commit()
            db.refresh(comment)
            return comment

        elif payload.user_action == 'reject':
            comment_query.update({'status': 'reject', 'last_update': datetime.datetime.now()}, synchronize_session=False)
            db.commit()
            db.refresh(comment)
            return comment

        elif payload.user_action == 'delete':
            comment_query.delete(synchronize_session=False)
            db.commit()
            response.status_code = status.HTTP_204_NO_CONTENT

    elif comment and comment.user_id == current_user.user_id:
        comment_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='شما صاحب این کامنت نیستید')


@router.get('/dashboard/comment/edit/{comment_id}')
def edit_comment(request: Request,
                 comment_id: int,
                 db: Session = Depends(get_db),
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                 ):
    comment = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id).first()
    context = {'request': request, 'user': current_user, 'comment': comment}
    return template.TemplateResponse('edit_comment.html', context)


@router.put('/dashboard/comment/edit/{comment_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def edit_comment(request: Request,
                 response: Response,
                 payload: schemas.posts.EditComment,
                 comment_id: int,
                 db: Session = Depends(get_db),
                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                 ):
    comment_query = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id)
    comment = comment_query.first()

    payload_dict = payload.dict()
    payload_dict.update({'last_update': datetime.datetime.now()})

    if comment and current_user.role == 'admin':
        payload_dict.update({'status': 'published'})
        try:
            comment_query.update(payload_dict, synchronize_session=False)
            db.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='خطا در ثبت')
    elif comment and current_user.user_id == comment.user_id:
        try:
            payload_dict.update({'status': 'pending'})
            comment_query.update(payload_dict, synchronize_session=False)
            db.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='خطا در ثبت')
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='شما مالک این کامنت نیستین')


# @router.delete('/users_comments/delete/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_comment(comment_id: int,
#                 db: Session = Depends(get_db),
#                 current_post: models.posts.Post = Depends(jwt_manager.get_current_user),
#                 current_user: models.auth.User = Depends(jwt_manager.get_current_user)
#                 ):
#     comment_query = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id)
#     comment = comment_query.first()
#
#     if comment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='comment not found')
#     else:
#         if comment.post_id == current_post.post_id or current_user.role == 'admin':
#             comment_query.delete(synchronize_session=False)
#             db.commit()
#         else:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not owner of this comment')

@router.get('/dashboard/post/manage')
def post_manage(request: Request,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):
    if current_user.role == 'admin':
        posts = db.query(models.posts.Post).order_by(models.posts.Post.status).all()
        context = {'request': request, 'posts': posts, 'user': current_user}
        return template.TemplateResponse('post_manage.html', context)


@router.post('/dashboard/post/manage/{post_id}')
def post_manage(response: Response,
                post_id: int,
                payload: schemas.posts.UserPostAction,
                db: Session = Depends(get_db),
                current_user: models.auth.User = Depends(jwt_manager.get_current_user)
                ):
    if current_user.role == 'admin':
        post_query = db.query(models.posts.Post).filter(models.posts.Post.post_id == post_id)

        payload_dict = payload.dict()
        payload_dict.pop('user_action')

        if payload.user_action == 'ok':
            try:
                payload_dict.update({'status': 'published', 'last_update': datetime.datetime.now()})
                post_query.update(payload_dict, synchronize_session=False)
                db.commit()
                response.status_code = status.HTTP_206_PARTIAL_CONTENT
                return
            except Exception:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif payload.user_action == 'reject':
            try:
                payload_dict.update({'status': 'reject', 'last_update': datetime.datetime.now()})
                post_query.update(payload_dict, synchronize_session=False)
                db.commit()
                response.status_code = status.HTTP_206_PARTIAL_CONTENT
                return
            except Exception:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif payload.user_action == 'delete':
            try:
                post_query.delete(synchronize_session=False)
                db.commit()
                response.status_code = status.HTTP_204_NO_CONTENT
                return
            except Exception:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return


# @router.delete('/comments/delete/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_comment(comment_id: int,
#                    db: Session = Depends(get_db),
#                    current_user: models.auth.User = Depends(jwt_manager.get_current_user)
#                    ):
#     comment_query = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id)
#     comment = comment_query.first()
#
#     if comment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='comment not found')
#     else:
#         if comment.user_id == current_user.user_id or current_user.role == 'admin':
#             comment_query.delete(synchronize_session=False)
#             db.commit()
#         else:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'your not owner of this post')


# @router.put('/comments/update/{comment_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
# def update_comment(response: Response, comment_id: int,
#                    payload: schemas.posts.updateComment,
#                    db: Session = Depends(get_db),
#                    current_user: models.auth.User = Depends(jwt_manager.get_current_user)
#                    ):
#     comment_query = db.query(models.posts.Comment).filter(models.posts.Comment.comment_id == comment_id)
#     comment = comment_query.first()
#
#     if comment is not None:
#         print(current_user.user_id)
#         print(comment.user_id)
#         if comment.user_id == current_user.user_id or current_user.role == "admin":
#             payload_dict = payload.dict()
#             payload_dict.update({"last_update": datetime.datetime.now()})
#             comment_query.update(payload_dict, synchronize_session=False)
#             db.commit()
#             return comment
#         else:
#             # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='you arent owner of this comment')
#             response.status_code = status.HTTP_404_NOT_FOUND
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='comment not found')


@router.get('/search')
def search(request: Request,
           query: Optional[str] = None,
           db: Session = Depends(get_db)
           ):
    print(query)
    if query:
        search_result = db.query(models.posts.Post).filter(models.posts.Post.title.contains(query)).all()
    else:
        search_result = None

    context = {'request': request, 'posts': search_result}
    return template.TemplateResponse('search_result.html', context)
