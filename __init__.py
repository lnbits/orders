import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import orders_generic_router
from .views_api import orders_api_router

orders_ext: APIRouter = APIRouter(
    prefix="/orders", tags=["Orders"]
)
orders_ext.include_router(orders_generic_router)
orders_ext.include_router(orders_api_router)


orders_static_files = [
    {
        "path": "/orders/static",
        "name": "orders_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def orders_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def orders_start():
    task = create_permanent_unique_task("ext_orders", wait_for_paid_invoices)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "orders_ext",
    "orders_start",
    "orders_static_files",
    "orders_stop",
]