from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException

from .schemas import DeleteMail, GetEmails, GetAddressMail
from .services import generate_value
from mails.models import Mail
from users.schemas import User
from users.services import buy_mail
from users.auth import get_current_active_user, check_limit_for_user
from domains.services import get_domains
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
    prefix = ""
    if login:
        if len(login) < 5:
            raise HTTPException(400, "Min 5 symbol in login")
    else:
        login = generate_value(8)
    if use_prefix:
        prefix = f"{generate_value(5)}."
    domains = await get_domains(type_domain=type_domain, use_prefix=use_prefix, limit=1)
    if not domains:
        raise HTTPException(400, "Not domain")
    domain = domains[0].domain
    price = domains[0].price
    mail = f"{login}@{prefix}{domain}"
    already_get_mail = await Mail.objects.get_or_none(mail=mail)
    if already_get_mail:
        if (
            not already_get_mail.is_active
            or datetime.now() > already_get_mail.time_expiries
        ):
            items = {
                "user": current_user.id,
                "is_active": True,
                "create_at": datetime.now(),
                "time_expiries": datetime.now() + timedelta(minutes=10),
                "emails": [],
            }
            await buy_mail(price, current_user)
            return await already_get_mail.update(**items)
        if already_get_mail.user.id != current_user.id:
            raise HTTPException(400, "Already create mail other user")
        return already_get_mail

    await buy_mail(price, current_user)
    return await Mail(mail=mail, user=current_user.id, price=price).save()
