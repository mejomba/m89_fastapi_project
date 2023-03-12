from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_id: int | None
    email: str | None
    username: str | None

    class Config:
        orm_mode = True


class CreatePost(BaseModel):
    title: str
    content: str


class ResponsePost(CreatePost):
    status: str
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True

