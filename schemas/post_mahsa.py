from pydantic import BaseModel
from datetime import datetime


class CreatePost(BaseModel):
    title: str
    content: str



class ResponsePost(CreatePost):
    status_id: str
    created_at: datetime

    class Config:
        orm_mode = True



class User(BaseModel):
    user_id: int | None
    email: str | None
    username: str | None

    class Config:
        orm_mode = True