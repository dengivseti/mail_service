from os import name
import odmantic
from typing import List, Optional, Union
from ormar import Model, Integer, String, Boolean, DateTime, ForeignKey
from db import MainMeta
from users.models import User
from users.schemas import UserConnect
from datetime import datetime


class Mail(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_ley=True)
    email: str = String(index=True, unique=True, nullable=False, max_length=88)
    user: Optional[UserConnect] = ForeignKey(User, nullable=False)
    create_at: datetime = DateTime(default=datetime.now)
    time_update: datetime = DateTime(default=datetime.now)
    mail: Optional[List[str]] = String(default=[])


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
