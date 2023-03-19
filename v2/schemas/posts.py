from pydantic import BaseModel, root_validator, validator
from datetime import datetime
from fastapi import HTTPException, status, File, UploadFile
from typing import Optional, Dict


class CommentBase(BaseModel):
    content: str
    parent_comment_id: int = None
    post_id: int

    @validator('content')
    def validate_content(cls, v):
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="comment content can't be empty")
        return v


class User(BaseModel):
    user_id: int | None
    email: str | None
    username: str | None
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True


class CreatePost(BaseModel):
    title: str
    content: str
    image: str | None = None

    @validator('title')
    def validate_title(cls, v):
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='title and content required')
        return v

    @validator('content')
    def validate_content(cls, v):
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='title and content required')
        return v


# class updatePost(BaseModel):
#     title: str
#     content: str
#     image: str | None = None
#
#     @validator('*')
#     def validate_title(cls, v):
#         if not v:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='title and content required')
#         return v


class updateComment(BaseModel):
    content: str

class ResponsePost(BaseModel):
    title: str
    content: str
    status: str
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True


class ResponseComment(BaseModel):
    content: str | None
    status: str | None
    post_related: ResponsePost | None

    class Config:
        orm_mode = True


class GetPost(BaseModel):
    title: str
    content: str
    post_comment: ResponseComment

    class Config:
        orm_mode = True


class UserCommentAction(BaseModel):
    user_action: str


class EditComment(BaseModel):
    content: str