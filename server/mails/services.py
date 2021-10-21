import random, string
from datetime import datetime
from fastapi import HTTPException, Depends
from users.auth import get_current_active_user

from users.models import User
from .models import Mail


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
