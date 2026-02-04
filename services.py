from lnbits.core.services.notifications import send_notification
from lnbits.settings import settings

from .crud import (
    create_extension_settings,
    get_extension_settings,
    update_extension_settings,
)
from .models import ExtensionSettings, Orders


def _parse_notify_emails(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [email.strip() for email in raw.split(",") if email.strip()]


def _build_order_link(base_url: str | None, order_id: str) -> str:
    if base_url:
        return f"{base_url.rstrip('/')}/orders/{order_id}"
    if settings.lnbits_baseurl:
        return f"{settings.lnbits_baseurl.rstrip('/')}/orders/{order_id}"
    return f"/orders/{order_id}"


async def _notify_customer(order: Orders, message: str | None, base_url: str | None) -> None:
    if not order.email and not order.npub:
        return
    link = _build_order_link(base_url, order.id)
    payload = f"{message} {link}" if message else link
    await send_notification(
        None,
        [order.npub] if order.npub else [],
        [order.email] if order.email else [],
        payload,
        "orders.customer",
    )


async def notify_new_order(settings: ExtensionSettings, order: Orders, base_url: str | None = None) -> None:
    amount_sat = order.amount_msat // 1000
    link = _build_order_link(base_url, order.id)
    message = (
        f"New order from {order.source} ({order.tpos_name or order.tpos_id or 'tpos'}) "
        f"- {amount_sat} sats - {order.payment_hash} - {link}"
    )
    await send_notification(
        settings.telegram,
        [settings.npub] if settings.npub else [],
        _parse_notify_emails(settings.email),
        message,
        "orders.new",
    )


async def notify_order_received(settings: ExtensionSettings, order: Orders, base_url: str | None) -> None:
    await _notify_customer(order, settings.message_order_received, base_url)


async def notify_order_shipped(settings: ExtensionSettings, order: Orders, base_url: str | None) -> None:
    await _notify_customer(order, settings.message_order_shipped, base_url)


async def get_settings(user_id: str) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    return settings


async def update_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, data)
    else:
        settings = await update_extension_settings(user_id, data)

    return settings
