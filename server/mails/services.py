import random, string
from loguru import logger
from datetime import datetime
from fastapi import HTTPException, Depends
from users.auth import get_current_active_user

from users.models import User
from .models import Mail, Email
from .schemas import EmailIn


def generate_value(count_symbol=5):
    return "".join([random.choice(string.ascii_lowercase) for i in range(count_symbol)])


async def is_active_mail(id: int, user: User):
    mail = await Mail.objects.get(id=id)
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
