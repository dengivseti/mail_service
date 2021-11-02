import random, string
from loguru import logger
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from users.auth import get_current_active_user

from users.models import User
from .models import Mail, Email
from .schemas import EmailIn, GetAddressMail, GetActiveMail
from domains.schemas import TypeDomain
from domains.services import get_domains
from users.services import buy_mail, delete_mail


def generate_value(count_symbol=5):
    return "".join([random.choice(string.ascii_lowercase) for i in range(count_symbol)])


async def is_active_mail(id: int, user: User):
    mail = await Mail.objects.select_related("emails").get(id=id)
    if not mail:
        return False
    if mail.user.id != user.id:
        return False
    if datetime.now() > mail.time_expiries or not mail.is_active:
        return False
    return mail


async def send_emails(email: EmailIn):
    to = email.get("to")
    _mail = await Mail.objects.select_related("emails").get_or_none(mail=to)
    if _mail and _mail.time_expiries > datetime.now() and _mail.is_active:
        email = await Email(**email).save()
        await _mail.emails.add(email)
        await _mail.update()


async def get_and_save_mail(
    current_user: User,
    login: Optional[str] = None,
    type_domain: Optional[TypeDomain] = None,
    use_prefix: Optional[bool] = None,
) -> GetAddressMail:
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


async def get_active_mails(user: User) -> list[GetActiveMail]:
    return await Mail.objects.filter(
        user=user.id, is_active=True, time_expiries__gt=datetime.now()
    ).all()
