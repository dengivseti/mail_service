from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class GetAddressMail(BaseModel):
    id: int
    mail: EmailStr
    time_expiries: datetime


class DeleteMail(BaseModel):
    mail: EmailStr
    is_active: bool


class Email(BaseModel):
    date: datetime
    expireAt: datetime
    subject: str
    from_at: str
    to: str
    html: str
    text: str
    textAsHtml: str


class GetEmails(BaseModel):
    id: int
    mail: EmailStr
    time_expiries: datetime
    emails: Optional[List[Email]]
