from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from users.schemas import User
from domains.models import TypeDomain
from users.auth import get_current_superuser, get_current_active_user
from .schemas import GetDomain, TypeDomain

from .services import get_domains


domain_router = APIRouter(prefix="/domain", tags=["domain"])


@domain_router.get("/getdomains", response_model=List[GetDomain])
async def get_random_domains(
    type_domain: Optional[TypeDomain] = None,
    use_prefix: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
):
    if type_domain:
        type_domain = type_domain.value
    domains = await get_domains(
        type_domain=type_domain, use_prefix=use_prefix, limit=10
    )
    return domains
