from pydantic import BaseModel, root_validator, validator
from datetime import datetime
from fastapi import HTTPException, status, File, UploadFile
from typing import Optional
from pydantic import BaseModel, validator


class Computer(BaseModel):
    brand: str
    storage_type: str
    ratings: list[int]

    @validator("*", pre=True)
    def uppercase_strings(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @validator("storage_type")
    def check_storage_type(cls, value):
        if value not in ("SSD", "HDD"):
            raise ValueError("Storage type can only be SSD or HDD.")
        return value

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

    @validator('*')
    def validate_title(cls, v):
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='title and content required')
        return v


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
    user_related: User | None

    class Config:
        orm_mode = True







class GetPost(BaseModel):
    title: str
    content: str
    post_comment: ResponseComment

    class Config:
        orm_mode = True
