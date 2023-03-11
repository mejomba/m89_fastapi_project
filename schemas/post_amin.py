from pydantic import BaseModel


class CommentBase(BaseModel):
    title: str
    content: str
    parent_comment_id: int = None
    post_id: int


class ResponseComment(BaseModel):
    title: str
    content: str
    status: str
# class CommentBase(BaseModel):
#     name:str
#     body:str
#     email:str
#
# class CommentList(CommentBase):
#     id: int
#     post_id:int
#     created_date: Optional[datetime.datetime]= Body(None)
#
#     class Config:
#         orm_mode= True
