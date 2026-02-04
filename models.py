from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, EmailStr, Field


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
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    tax_included: bool | None = None
    tax_value: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    address: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    npub: str | None = None
    weight: str | None = None
    paid: bool = False
    shipped: bool = False
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
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    tax_included: bool | None = None
    tax_value: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    address: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    npub: str | None = None
    weight: str | None = None
    paid: bool = False
    shipped: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrdersResponse(BaseModel):
    id: str
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
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    tax_included: bool | None = None
    tax_value: float | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    address: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    npub: str | None = None
    weight: str | None = None
    paid: bool = False
    shipped: bool = False
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
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    items: list[dict] = Field(default_factory=list)
    notes: dict | None = None
    address: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    npub: str | None = None
    weight: str | None = None
    paid: bool = False
    shipped: bool = False
    business_name: str | None = None
    business_address: str | None = None
    created_at: datetime | None = None


class OrdersFilters(FilterModel):
    __search_fields__ = [
        "source",
        "tpos_id",
        "tpos_name",
        "payment_hash",
        "checking_id",
        "address",
        "email",
        "phone",
    ]

    __sort_fields__ = [
        "source",
        "tpos_name",
        "amount_msat",
        "paid",
        "shipped",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None
    paid: bool | None = None
    shipped: bool | None = None


############################ Settings #############################
class ExtensionSettings(BaseModel):
    npub: str | None
    telegram: str | None
    email: str | None
    fiat_denomination: str | None = None
    message_order_received: str | None = "Thank you for your order please check here to see when it is shipped"
    message_order_shipped: str | None = "Your order has been shipped!"
    business_name: str | None = None
    business_address: str | None = None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("False" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str
