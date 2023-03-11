from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from schemas import post_mahsa
from models import posts,auth


router = APIRouter(tags=['posts'])


@router.post('/posts'/, response_model=post_mahsa.User)
def crate_post(Post:post_mahsa.Post, db: session=Depends(get_db)):
    db_post = db.query(posts.Post).filter(posts.Post.post_id==Post.post_id)
    if db_post:
       raise HTTPException(status_code=400, detail='post is already exists')
    Post = posts.Post(post_id=Post.post_id, title=Post.title, content=Post.content)
    db.add(Post)
    db.commit()
    db.refresh(Post)
    return db_post

@router.post('/posts'/, response_model=post_mahsa.User)
def show_post(Post:post_mahsa.Post, db: session=Depends(get_db)):
    db_post = db.query(posts.Post).filter(posts.Post.post_id==Post.post_id)
    if db_post is None:
       raise HTTPException(status_code=400, detail='post not found')
    return db_post


@router.post('/posts'/, response_model=post_mahsa.User)
def raed_post_user(User:post_mahsa.User, db: session=Depends(get_db)):
    db_post = db.query(posts.Post).filter(posts.Post.user_id==User.user_id)
    if db_post:
       return db_post
    raise HTTPException(status_code=400, detail='This user has no post')


