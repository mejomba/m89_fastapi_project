from pydantic import BaseModel
from datetime import datetime


class Get_post(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
