from pydantic import BaseModel


class Post(BaseModel):
    post_id: int
    title: str
    content: str


class User(BaseModel):
    user_id: int | None
    email: str | None
    username: str | None

    class Config:
        orm_mode = True