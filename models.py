from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Orders ############################
class CreateOrders(BaseModel):
    source: str
    tpos_id: str | None = None
    tpos_name: str | None = None
    payment_hash: str
    checking_id: str
    amount_msat: int
    fee_msat: int
    memo: str | None = None
    paid_in_fiat: bool = False
    currency: str | None = None
    exchange_rate: float | None = None
    tax_included: bool | None = None
    tax_value: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    created_at: datetime | None = None


class Orders(BaseModel):
    id: str
    user_id: str
    source: str
    tpos_id: str | None = None
    tpos_name: str | None = None
    payment_hash: str
    checking_id: str
    amount_msat: int
    fee_msat: int
    memo: str | None = None
    paid_in_fiat: bool = False
    currency: str | None = None
    exchange_rate: float | None = None
    tax_included: bool | None = None
    tax_value: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PublicOrders(BaseModel):
    id: str
    source: str
    tpos_name: str | None = None
    payment_hash: str
    amount_msat: int
    paid_in_fiat: bool = False
    currency: str | None = None
    exchange_rate: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    created_at: datetime | None = None


class OrdersFilters(FilterModel):
    __search_fields__ = [
        "source",
        "tpos_id",
        "tpos_name",
        "payment_hash",
        "checking_id",
    ]

    __sort_fields__ = [
        "source",
        "tpos_name",
        "amount_msat",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


############################ Settings #############################
class ExtensionSettings(BaseModel):
    npub: str | None
    telegram: str | None
    email: str | None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("False" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str
