from os import name
import odmantic
from typing import List, Optional, Union, Dict
from ormar import Model, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON
from db import MainMeta
from users.models import User
from users.schemas import UserConnect
from datetime import datetime, timedelta
import pydantic


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
    emails: pydantic.Json = JSON(default=[])


class MailMongo(odmantic.Model):
    date: datetime
    expireAt: datetime
    subject: str
    from_at: str
    to: str
    html: str
    text: str
    textAsHtml: str

    class Config:
        collection = "Mail"
