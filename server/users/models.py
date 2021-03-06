from ormar import Model, Integer, String, Boolean, DateTime, Float
from db import MainMeta
from uuid import uuid4
from datetime import datetime


class User(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    email = String(index=True, unique=True, nullable=False, max_length=88)
    password = String(nullable=False, max_length=255)
    is_active = Boolean(default=True, nullable=False)
    is_superuser = Boolean(default=False, nullable=False)
    api_key = String(default=uuid4().hex, max_length=150, nullable=False)
    max_thread = Integer(
        default=50,
    )
    thread = Integer(default=0)
    balance = Float(default=0)
    create_at: datetime = DateTime(default=datetime.now)
