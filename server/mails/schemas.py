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


class EmailIn(BaseModel):
    subject: str
    from_at: str
    to: str
    html: str
    text: str
    textAsHtml: str


class EmailOut(EmailIn):
    id: int
    create_at: datetime


class GetEmails(BaseModel):
    id: int
    mail: EmailStr
    time_expiries: datetime
    emails: Optional[List[EmailOut]]
