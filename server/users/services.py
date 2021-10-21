import os
import re
from typing import Optional
from datetime import datetime, timedelta
from loguru import logger
from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException
from .models import User


SECRET = os.getenv("SECRET_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password):
    return pwd_context.encrypt(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Make sure your password is at lest 8 letters")
    elif re.search("[0-9]", password) is None:
        raise HTTPException(400, "Make sure your password has a number in it")
    elif re.search("[A-Z]", password) is None:
        raise HTTPException(400, "Make sure your password has a capital letter in it")
    else:
        return encrypt_password(password)


async def buy_mail(price: float, user: User):
    user.balance -= price
    user.thread += 1
    await user.update()


async def delete_mail(price: float, user: User):
    user.balance += price
    user.thread -= 1
    await user.update()
