from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import oauth2
from requests import Session

from database_manager import get_db
from models.auth import User
from schemas import post_hesam

router = APIRouter(tags=['posts'])


@router.get("/posts", response_model=List[post_hesam.Get_post])
def user_post(
        db: Session = Depends(get_db),
        current_user: User = Depends(oauth2.get_current_user),
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = ""):
    posts: List[post_hesam.Get_post] = db.query(post_hesam.Get_post). \
        filter(post_hesam.Get_post.user_id == current_user.id). \
        filter(post_hesam.Get_post.title.contains(search)). \
        limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", status_code=200)
def get_post(
        db: Session = Depends(get_db),
        current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(post_hesam.Get_post).filter(post_hesam.Get_post.user_id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return {'message': post}
