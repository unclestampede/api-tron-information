from datetime import datetime

from pydantic import UUID4, Field

from app.models.utils import ApiModel


class TronInfoBase(ApiModel):
    address: str = Field(..., description="")
    balance: float = Field(..., description="")
    energy: int = Field(..., description="")
    bandwidth: int = Field(..., description="")


class TronInfoCreate(TronInfoBase):
    pass


class TronInfoGet(TronInfoBase):
    created: datetime = Field(..., description="")
    updated: datetime = Field(..., description="")
