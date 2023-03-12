from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas, models
from database_manager import get_db

router = APIRouter(tags=['posts'])


@router.post('/comment', response_model=schemas.post_amin.ResponseComment)
def create_comment(payload: schemas.post_amin.CommentBase, db: Session = Depends(get_db)):
    payload_dict = payload.dict()
    payload_dict.update({'status': 'pending', 'user_id': 1})
    new_comment = models.posts.Post(**payload_dict)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
