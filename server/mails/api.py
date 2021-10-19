from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException

from .schemas import DeleteMail, GetEmails, GetAddressMail
from .services import generate_value
from mails.models import Mail
from users.schemas import User
from users.auth import get_current_active_user
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
    current_user: User = Depends(get_current_active_user),
):
    # TODO work with balance and thread and max_thread
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
    try:
        return await Mail(mail=mail, user=current_user.id, price=price).save()

    except Exception as e:
        raise HTTPException(400, "Already create mail other user")
