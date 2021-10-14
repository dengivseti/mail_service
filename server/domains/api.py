from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Query
from users.schemas import User
from domains.models import TypeDomain
from users.auth import get_current_superuser, get_current_active_user
from .schemas import GetDomain, TypeDomain
from .models import Domain
from loguru import logger
from random import shuffle


domain_router = APIRouter(prefix="/domain", tags=["domain"])


@domain_router.get("/getdomains", response_model=List[GetDomain])
async def get_domains(
    type_domain: Optional[TypeDomain] = None,
    current_user: User = Depends(get_current_active_user),
):
    if type_domain:
        domains = await Domain.objects.filter(
            is_active=True,
            is_baned=False,
            type_domain=type_domain.value,
        ).all()
    else:
        domains = await Domain.objects.filter(
            is_active=True,
            is_baned=False,
        ).all()
    if domains:
        shuffle(domains)

    return domains[:10]
