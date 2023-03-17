from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, validator, BaseSettings
from fastapi import HTTPException, status


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
        if not v:
            return v
        if not v.isdigit():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='phone not valid')
        if len(v) != 11:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='phone not valid')
        return v


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
