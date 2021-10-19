from typing import Union, Optional

from db import MainMeta
from ormar import Model, String, Boolean, DateTime, Integer, ForeignKey, Float
from datetime import datetime

from users.models import User
from users.schemas import UserConnect

from .schemas import TypeDomain


class Domain(Model):
    class Meta(MainMeta):
        pass

    id: int = Integer(primary_key=True)
    domain: str = String(index=True, unique=True, nullable=False, max_length=88)
    is_active: bool = Boolean(default=False, nullable=False)
    is_check: bool = Boolean(default=False, nullable=False)
    is_baned: bool = Boolean(default=False, nullable=False)
    create_at: datetime = DateTime(default=datetime.now)
    last_check: datetime = DateTime(default=datetime.now)
    type_domain: Optional[str] = String(
        max_length=100, choices=list(TypeDomain), default=TypeDomain.other.value
    )
    price: int = Float(default=0.01)
    use_prefix: Optional[bool] = Boolean(default=False, nullable=False)
    user: Optional[UserConnect] = ForeignKey(User, nullable=True)
