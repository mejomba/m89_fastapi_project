from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, SecretStr


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    # role: str = 'regular_user'
    phone: Optional[str] | None = None
    # created_at: Optional[datetime] = None
    # last_update: Optional[datetime] = None

    class Config:
        orm_mode = True


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
