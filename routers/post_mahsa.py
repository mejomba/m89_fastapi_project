from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models.posts
from schemas import post_mahsa
from models import posts,auth
from database_manager import get_db
import jwt_manager

router = APIRouter(tags=['posts'])



@router.post('/post', response_model=post_mahsa.ResponsePost)
def crate_post(payload:post_mahsa.CreatePost,
               db: Session = Depends(get_db),
               current_user: auth.User = Depends(jwt_manager.get_current_user)):
    payload_dict = payload.dict()
    if current_user.role == "admin":
        payload_dict.update({'status': 'published', 'user_id': current_user.user_id})
    elif current_user.role == "writer":
        payload_dict.update({'status': 'pending', 'user_id': current_user.user_id})
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')

    new_post = posts.Post(**payload_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @router.post('/posts', response_model=post_mahsa.User)
# def show_post(Post:post_mahsa.Post, db: session=Depends(get_db)):
#     db_post = db.query(posts.Post).filter(posts.Post.post_id==Post.post_id)
#     if db_post is None:
#        raise HTTPException(status_code=400, detail='post not found')
#     return db_post
#
#
# @router.post('/posts'/, response_model=post_mahsa.User)
# def raed_post_user(User:post_mahsa.User, db: session=Depends(get_db)):
#     db_post = db.query(posts.Post).filter(posts.Post.user_id==User.user_id)
#     if db_post:
#        return db_post
#     raise HTTPException(status_code=400, detail='This user has no post')



