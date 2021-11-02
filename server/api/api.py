from fastapi import APIRouter, Depends, Request, Query, HTTPException
from loguru import logger
from typing import Optional

from users.schemas import UserInfo
from users.models import User
from .auth import get_current_active_api_user, check_limit_for_user
from mails.schemas import GetAddressMail, GetEmails, DeleteMail, GetActiveMail
from mails.services import (
    get_and_save_mail,
    is_active_mail,
    delete_mail,
    get_active_mails,
)
from domains.services import TypeDomain


api_router = APIRouter(prefix="/api/v1", tags=["API"])


@api_router.get("/info", response_model=UserInfo)
async def get_information(
    api_key: str,
    current_user: User = Depends(get_current_active_api_user),
):
    return current_user


@api_router.get("/get_mail", response_model=GetAddressMail)
async def get_mail(
    api_key: str,
    login: Optional[str] = None,
    type_domain: Optional[TypeDomain] = None,
    use_prefix: Optional[bool] = None,
    current_user: User = Depends(check_limit_for_user),
):
    return await get_and_save_mail(current_user, login, type_domain, use_prefix)


@api_router.get("/{id}/delete", status_code=201, response_model=DeleteMail)
async def delete_mail_id(
    id: int, api_key: str, current_user: User = Depends(get_current_active_api_user)
):
    mail = await is_active_mail(id, current_user)
    if not mail:
        raise HTTPException(400, detail="Mail not found")
    await mail.update(is_active=False)
    if not mail.emails:
        logger.error(current_user.dict())
        await delete_mail(mail.price, current_user)
    return mail


@api_router.get("/mail/{id}", status_code=200, response_model=GetEmails)
async def get_emails(
    id: int, api_key: str, current_user: User = Depends(get_current_active_api_user)
):
    mail = await is_active_mail(id, current_user)
    if not mail:
        raise HTTPException(400, detail="Mail not found")
    if mail.emails:
        return mail
    return mail


@api_router.get("/active_mails", status_code=200, response_model=list[GetActiveMail])
async def get_active_mail(
    api_key: str, current_user: User = Depends(get_current_active_api_user)
):
    return await get_active_mails(current_user)
