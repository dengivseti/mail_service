from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from .auth import (
    authenticate_user,
    get_current_active_user,
)
from .services import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, encrypt_password
from .schemas import Token, UserCreate, User, UserOut
from . import models

user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.post("/signup", status_code=201, response_model=User)
async def create_user(user: UserCreate):
    _user = await models.User.objects.get_or_none(email=user.email)
    if _user:
        raise HTTPException(400, "User already register")
    hash_password = encrypt_password(user.password)
    return await models.User.objects.create(email=user.email, password=hash_password)


@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
