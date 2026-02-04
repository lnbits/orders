# Description: This file contains the extensions API endpoints.
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.core.models.users import AccountId
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_account_exists,
    check_account_id_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_orders,
    delete_orders,
    get_orders,
    get_orders_by_id,
    get_orders_paginated,
    update_orders,
)
from .models import (
    CreateOrders,
    ExtensionSettings,
    Orders,
    OrdersFilters,
    PublicOrders,
)
from .services import (
    get_settings,
    update_settings,
)

orders_filters = parse_filters(OrdersFilters)
orders_api_router = APIRouter()


############################# Orders #############################
@orders_api_router.post("/api/v1/orders", status_code=HTTPStatus.CREATED)
async def api_create_orders(
    data: CreateOrders,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Orders:
    orders = await create_orders(account_id.id, data)
    return orders


@orders_api_router.put("/api/v1/orders/{orders_id}", status_code=HTTPStatus.CREATED)
async def api_update_orders(
    orders_id: str,
    data: CreateOrders,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Orders:
    orders = await get_orders(account_id.id, orders_id)
    if not orders:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Orders not found.")
    if orders.user_id != account_id.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this orders.")
    orders = await update_orders(Orders(**{**orders.dict(), **data.dict()}))
    return orders


@orders_api_router.get(
    "/api/v1/orders/paginated",
    name="Orders List",
    summary="get paginated list of orders",
    response_description="list of orders",
    openapi_extra=generate_filter_params_openapi(OrdersFilters),
    response_model=Page[Orders],
)
async def api_get_orders_paginated(
    account_id: AccountId = Depends(check_account_id_exists),
    filters: Filters = Depends(orders_filters),
) -> Page[Orders]:

    return await get_orders_paginated(
        user_id=account_id.id,
        filters=filters,
    )


@orders_api_router.get(
    "/api/v1/orders/{orders_id}",
    name="Get Orders",
    summary="Get the orders with this id.",
    response_description="An orders or 404 if not found",
    response_model=Orders,
)
async def api_get_orders(
    orders_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Orders:

    orders = await get_orders(account_id.id, orders_id)
    if not orders:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Orders not found.")

    return orders


@orders_api_router.get(
    "/api/v1/orders/{orders_id}/public",
    name="Get Public Orders",
    summary="Get the public orders with this id." "This is a public endpoint.",
    response_description="An orders or 404 if not found",
    response_model=PublicOrders,
)
async def api_get_public_orders(orders_id: str) -> PublicOrders:

    orders = await get_orders_by_id(orders_id)
    if not orders:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Orders not found.")

    return PublicOrders(**orders.dict())


@orders_api_router.delete(
    "/api/v1/orders/{orders_id}",
    name="Delete Orders",
    summary="Delete the orders.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_orders(
    orders_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> SimpleStatus:

    await delete_orders(account_id.id, orders_id)
    return SimpleStatus(success=True, message="Orders Deleted")


############################ Settings #############################
@orders_api_router.get(
    "/api/v1/settings",
    name="Get Settings",
    summary="Get the settings for the current user.",
    response_description="The settings or 404 if not found",
    response_model=ExtensionSettings,
)
async def api_get_settings(
    account_id: AccountId = Depends(check_account_id_exists),
) -> ExtensionSettings:
    user_id = "admin" if ExtensionSettings.is_admin_only() else account_id.id
    return await get_settings(user_id)


@orders_api_router.put(
    "/api/v1/settings",
    name="Update Settings",
    summary="Update the settings for the current user.",
    response_description="The updated settings.",
    response_model=ExtensionSettings,
)
async def api_update_extension_settings(
    data: ExtensionSettings,
    account: User = Depends(check_account_exists),
) -> ExtensionSettings:
    if ExtensionSettings.is_admin_only() and not account.admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            "Only admins can update settings.",
        )
    user_id = "admin" if ExtensionSettings.is_admin_only() else account.id
    return await update_settings(user_id, data)
