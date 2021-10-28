from os import name
from typing import List, Optional, Union, Dict
from ormar import (
    Model,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    ManyToMany,
)
from .schemas import EmailOut
from db import MainMeta
from users.models import User
from users.schemas import UserConnect
from datetime import datetime, timedelta


class EmailFromMail(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)


class Email(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    create_at: datetime = DateTime(default=datetime.now)
    time_expiries: datetime = DateTime(default=datetime.now() + timedelta(minutes=10))
    subject: str = String(nullable=False, max_length=8000)
    from_at: str = String(nullable=False, max_length=8000)
    to: str = String(nullable=False, max_length=8000)
    html: str = String(nullable=False, max_length=8000)
    text: str = String(nullable=False, max_length=8000)
    textAsHtml: str = String(nullable=False, max_length=10000)


class Mail(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    mail: str = String(index=True, unique=True, nullable=False, max_length=88)
    user: Optional[UserConnect] = ForeignKey(User, nullable=False)
    is_active: bool = Boolean(default=True)
    create_at: datetime = DateTime(default=datetime.now)
    time_expiries: datetime = DateTime(default=datetime.now() + timedelta(minutes=10))
    price: float = Float(default=0)
    emails: Optional[List[EmailOut]] = ManyToMany(
        Email, related_name="emails", through=EmailFromMail
    )
