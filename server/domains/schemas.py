from typing import Optional, List
from enum import Enum
from pydantic import BaseModel


class TypeDomain(str, Enum):
    freenom = "freenom"
    other = "other"


class GetDomain(BaseModel):
    domain: str
    type_domain: str
    use_prefix: bool
    price: float


class AddDomain(BaseModel):
    domain: str
    type_domain: Optional[TypeDomain]
    use_prefix: Optional[bool]
    price: Optional[float]


class ListAddDomain(BaseModel):
    domain: List[str]
    type_domain: Optional[TypeDomain]
    use_prefix: Optional[bool]
