from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.posts
from schemas import post_mahsa
from models import posts,auth
from database_manager import get_db


router = APIRouter(tags=['posts'])


@router.post('/posts', response_model=post_mahsa.ResponsePost)
def crate_post(payload:post_mahsa.CreatePost, db: Session=Depends(get_db)):

@router.post('/posts/{post_id}', response_model=post_mahsa.User)
def show_post(Post:post_mahsa.Post, db: session=Depends(get_db)):
    db_post = db.query(posts.Post).filter(posts.Post.post_id==Post.post_id)
    if db_post is None:
       raise HTTPException(status_code=400, detail='post not found')
    return db_post


@router.post('/posts/{user_id}', response_model=post_mahsa.User)
def raed_post_user(current_user:User:post_mahsa.User, db: session=Depends(get_db)):
    db_post = db.query(posts.Post).filter(auth.User.user_id==current_user.user_id).filter(posts.Post.user_id==User.user_id)
    if db_post:
       return db_post
    raise HTTPException(status_code=400, detail='This user has no post')


