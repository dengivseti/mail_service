from typing import Optional
from .schemas import TypeDomain
from .models import Domain
from loguru import logger
from random import shuffle


async def get_domains(
    type_domain: Optional[TypeDomain] = None,
    use_prefix: Optional[bool] = None,
    limit: int = 0,
):
    if type_domain:
        domains = await Domain.objects.filter(
            is_active=True, is_baned=False, type_domain=type_domain
        ).all()
    else:
        domains = await Domain.objects.filter(is_active=True, is_baned=False).all()
    if not use_prefix is None:
        domains = [domain for domain in domains if domain.use_prefix == use_prefix]
    if domains:
        shuffle(domains)
    if limit:
        return domains[:limit]
    return domains
