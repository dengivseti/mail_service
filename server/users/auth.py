from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger


from .schemas import UserInBD, TokenData
from .models import User
from .services import verify_password, SECRET, ALGORITHM
from mails.models import Mail
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_user(email: str) -> UserInBD:
    user = await User.objects.get_or_none(email=email)
    if user:
        return user


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_limit_for_user(current_user: User = Depends(get_current_active_user)):
    mails = await Mail.objects.filter(
        user=current_user.id, time_expiries__gt=datetime.now(), is_active=True
    ).all()
    await current_user.update(thread=len(mails))
    if current_user.thread >= current_user.max_thread:
        raise HTTPException(400, detail="Max limit thread")
    if current_user.balance <= 0:
        raise HTTPException(400, detail="Not balance")
    return current_user
