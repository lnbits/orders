# Description: This file contains the CRUD operations for talking to the database.


from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    CreateOrders,
    ExtensionSettings,
    Orders,
    OrdersFilters,
    UserExtensionSettings,
)

db = Database("ext_orders")


########################### Orders ############################
async def create_orders(user_id: str, data: CreateOrders) -> Orders:
    orders = Orders(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("orders.orders", orders)
    return orders


async def get_orders(
    user_id: str,
    orders_id: str,
) -> Orders | None:
    return await db.fetchone(
        """
            SELECT * FROM orders.orders
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": orders_id, "user_id": user_id},
        Orders,
    )


async def get_orders_by_id(
    orders_id: str,
) -> Orders | None:
    return await db.fetchone(
        """
            SELECT * FROM orders.orders
            WHERE id = :id
        """,
        {"id": orders_id},
        Orders,
    )


async def get_orders_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM orders.orders
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_orders_paginated(
    user_id: str | None = None,
    filters: Filters[OrdersFilters] | None = None,
) -> Page[Orders]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM orders.orders",
        where=where,
        values=values,
        filters=filters,
        model=Orders,
    )


async def update_orders(data: Orders) -> Orders:
    await db.update("orders.orders", data)
    return data


async def delete_orders(user_id: str, orders_id: str) -> None:
    await db.execute(
        """
            DELETE FROM orders.orders
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": orders_id, "user_id": user_id},
    )


############################ Settings #############################
async def create_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.insert("orders.extension_settings", settings)
    return settings


async def get_extension_settings(
    user_id: str,
) -> ExtensionSettings | None:
    return await db.fetchone(
        """
            SELECT * FROM orders.extension_settings
            WHERE id = :user_id
        """,
        {"user_id": user_id},
        ExtensionSettings,
    )


async def update_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.update("orders.extension_settings", settings)
    return settings
