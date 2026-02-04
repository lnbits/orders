from lnbits.core.services.notifications import send_notification

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


async def notify_new_order(settings: ExtensionSettings, order: Orders) -> None:
    amount_sat = order.amount_msat // 1000
    message = (
        f"New order from {order.source} ({order.tpos_name or order.tpos_id or 'tpos'}) "
        f"- {amount_sat} sats - {order.payment_hash}"
    )
    await send_notification(
        settings.telegram,
        [settings.npub] if settings.npub else [],
        _parse_notify_emails(settings.email),
        message,
        "orders.new",
    )


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
