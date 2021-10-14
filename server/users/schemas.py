from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr


class User(BaseModel):
    email: EmailStr
    max_thread: int
    thread: int
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(User):
    password: str


class UserOut(User):
    id: int
    api_key: str


class UserConnect(BaseModel):
    id: int
    email: EmailStr
    is_active: bool


class UserInBD(UserOut):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
