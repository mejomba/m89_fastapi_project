from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, validator
from fastapi import HTTPException, status
import re


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] | None = None

    class Config:
        orm_mode = True

    @validator('phone')
    def validate_phone(cls, v):
        pattern = r'(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}'
        if not v:
            return v
        if not re.match(pattern, v):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='phone not valid')
        return v


class UpdateUser(CreateUser):
    image: str | None = None
    remove_image: bool | None = None
    password: Optional[str]


class ResponseUser(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangeUserRole(BaseModel):
    user_request_action: str


class ContactUs(BaseModel):
    name: str
    email: EmailStr
    content: str
