from fastapi import Depends, HTTPException, status, Request
from datetime import datetime

from loguru import logger

from users.schemas import UserInBD
from users.models import User
from mails.models import Mail

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_api_user(api_key: str) -> UserInBD:
    user = await User.objects.get_or_none(api_key=api_key)
    if user and user.is_active:
        return user


async def get_current_active_api_user(request: Request):
    api_key: str = request.query_params.get("api_key")
    if not api_key:
        raise credentials_exception
    user = await get_api_user(api_key)
    if not user:
        raise credentials_exception
    return user


async def check_limit_for_user(
    current_user: User = Depends(get_current_active_api_user),
):
    mails = await Mail.objects.filter(
        user=current_user.id, time_expiries__gt=datetime.now(), is_active=True
    ).all()
    logger.warning(mails)
    await current_user.update(thread=len(mails))
    if current_user.thread >= current_user.max_thread:
        raise HTTPException(400, detail="Max limit thread")
    if current_user.balance <= 0:
        raise HTTPException(400, detail="Not balance")
    return current_user
