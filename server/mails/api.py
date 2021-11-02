from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException

from .schemas import DeleteMail, GetEmails, GetAddressMail
from .services import generate_value, is_active_mail, get_and_save_mail
from mails.models import Mail
from users.schemas import User
from users.services import buy_mail, delete_mail
from users.auth import get_current_active_user, check_limit_for_user

from domains.schemas import TypeDomain
from uuid import uuid4
from loguru import logger

mail_router = APIRouter(prefix="/mail", tags=["mail"])


@mail_router.get("/get", status_code=201, response_model=GetAddressMail)
async def get_mail(
    login: Optional[str] = None,
    type_domain: Optional[TypeDomain] = None,
    use_prefix: Optional[bool] = None,
    current_user: User = Depends(check_limit_for_user),
):
    return await get_and_save_mail(current_user, login, type_domain, use_prefix)


@mail_router.get("/{id}/delete", status_code=201, response_model=DeleteMail)
async def delete_mail_id(
    id: int, current_user: User = Depends(get_current_active_user)
):
    mail = await is_active_mail(id, current_user)
    if not mail:
        raise HTTPException(400, detail="Mail not found")
    await mail.update(is_active=False)
    if not mail.emails:
        logger.error(current_user.dict())
        await delete_mail(mail.price, current_user)
    return mail


@mail_router.get("/{id}", status_code=200, response_model=GetEmails)
async def get_emails(id: int, current_user: User = Depends(get_current_active_user)):
    mail = await is_active_mail(id, current_user)
    if not mail:
        raise HTTPException(400, detail="Mail not found")
    if mail.emails:
        return mail
    return mail
