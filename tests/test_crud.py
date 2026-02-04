from datetime import datetime, timezone
from uuid import uuid4

import pytest

from orders.crud import (  # type: ignore[import]
    create_orders,
    delete_orders,
    get_orders,
    get_orders_by_id,
    get_orders_ids_by_user,
    get_orders_paginated,
    update_orders,
)
from orders.models import (  # type: ignore[import]
    CreateOrders,
    Orders,
)


@pytest.mark.asyncio
async def test_create_and_get_orders():
    user_id = uuid4().hex

    data = CreateOrders(
        source="tpos",
        tpos_id="tpos_1",
        tpos_name="Front Counter",
        payment_hash="ph_1",
        checking_id="chk_1",
        amount_msat=1500,
        fee_msat=0,
        memo="Order 1",
        paid_in_fiat=False,
        currency="USD",
        exchange_rate=25000.0,
        tax_included=True,
        tax_value=0.1,
        items=[{"id": "item_1", "title": "Coffee", "quantity": 1}],
        notes={"Coffee": "Oat milk"},
        created_at=datetime.now(timezone.utc),
    )
    orders_one = await create_orders(user_id, data)
    assert orders_one.id is not None
    assert orders_one.user_id == user_id

    orders_one = await get_orders(user_id, orders_one.id)
    assert orders_one.id is not None
    assert orders_one.user_id == user_id
    assert orders_one.source == data.source
    assert orders_one.items == data.items
    assert orders_one.payment_hash == data.payment_hash
    assert orders_one.amount_msat == data.amount_msat
    assert orders_one.tpos_name == data.tpos_name

    data = CreateOrders(
        source="tpos",
        tpos_id="tpos_2",
        tpos_name="Back Counter",
        payment_hash="ph_2",
        checking_id="chk_2",
        amount_msat=2500,
        fee_msat=0,
        memo="Order 2",
        paid_in_fiat=False,
        currency="USD",
        exchange_rate=25000.0,
        tax_included=False,
        tax_value=0.0,
        items=[{"id": "item_2", "title": "Tea", "quantity": 2}],
        notes={"Tea": "No sugar"},
        created_at=datetime.now(timezone.utc),
    )
    orders_two = await create_orders(user_id, data)
    assert orders_two.id is not None
    assert orders_two.user_id == user_id

    orders_list = await get_orders_ids_by_user(user_id=user_id)
    assert len(orders_list) == 2

    orders_page = await get_orders_paginated(user_id=user_id)
    assert orders_page.total == 2
    assert len(orders_page.data) == 2

    await delete_orders(user_id, orders_one.id)
    orders_list = await get_orders_ids_by_user(user_id=user_id)
    assert len(orders_list) == 1

    orders_page = await get_orders_paginated(user_id=user_id)
    assert orders_page.total == 1
    assert len(orders_page.data) == 1


@pytest.mark.asyncio
async def test_update_orders():
    user_id = uuid4().hex

    data = CreateOrders(
        source="tpos",
        tpos_id="tpos_1",
        tpos_name="Front Counter",
        payment_hash="ph_3",
        checking_id="chk_3",
        amount_msat=1500,
        fee_msat=0,
        memo="Order 3",
        paid_in_fiat=False,
        currency="USD",
        exchange_rate=25000.0,
        tax_included=True,
        tax_value=0.1,
        items=[{"id": "item_1", "title": "Coffee", "quantity": 1}],
        notes={"Coffee": "Oat milk"},
        created_at=datetime.now(timezone.utc),
    )
    orders_one = await create_orders(user_id, data)
    assert orders_one.id is not None
    assert orders_one.user_id == user_id

    orders_one = await get_orders(user_id, orders_one.id)
    assert orders_one.id is not None
    assert orders_one.user_id == user_id
    assert orders_one.source == data.source
    assert orders_one.items == data.items
    assert orders_one.payment_hash == data.payment_hash
    assert orders_one.amount_msat == data.amount_msat
    assert orders_one.tpos_name == data.tpos_name

    data_updated = CreateOrders(
        source="tpos",
        tpos_id="tpos_1",
        tpos_name="Front Counter",
        payment_hash="ph_3",
        checking_id="chk_3",
        amount_msat=3500,
        fee_msat=0,
        memo="Order 3 updated",
        paid_in_fiat=False,
        currency="USD",
        exchange_rate=25000.0,
        tax_included=True,
        tax_value=0.2,
        items=[{"id": "item_1", "title": "Coffee", "quantity": 2}],
        notes={"Coffee": "Oat milk"},
        created_at=datetime.now(timezone.utc),
    )
    orders_updated = Orders(**{**orders_one.dict(), **data_updated.dict()})

    await update_orders(orders_updated)
    orders_one = await get_orders_by_id(orders_one.id)
    assert orders_one.source == orders_updated.source
    assert orders_one.items == orders_updated.items
    assert orders_one.payment_hash == orders_updated.payment_hash
    assert orders_one.amount_msat == orders_updated.amount_msat
    assert orders_one.tpos_name == orders_updated.tpos_name
