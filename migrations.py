empty_dict: dict[str, str] = {}


async def m001_extension_settings(db):
    """
    Initial settings table.
    """

    await db.execute(
        f"""
        CREATE TABLE orders.extension_settings (
            id TEXT NOT NULL,
            npub TEXT,
            telegram TEXT,
            email TEXT,
            fiat_denomination TEXT,
            message_order_received TEXT,
            message_order_shipped TEXT,
            business_name TEXT,
            business_address TEXT,
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m002_orders(db):
    """
    Initial orders table.
    """

    await db.execute(
        f"""
        CREATE TABLE orders.orders (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            source TEXT NOT NULL,
            tpos_id TEXT,
            tpos_name TEXT,
            payment_hash TEXT NOT NULL,
            checking_id TEXT NOT NULL,
            amount_msat {db.big_int} NOT NULL,
            fee_msat {db.big_int} NOT NULL,
            memo TEXT,
            paid_in_fiat BOOLEAN NOT NULL DEFAULT false,
            currency TEXT,
            exchange_rate REAL,
            fiat_amount REAL,
            fiat_currency TEXT,
            tax_included BOOLEAN,
            tax_value REAL,
            items TEXT NOT NULL DEFAULT '[]',
            notes TEXT,
            address TEXT,
            email TEXT,
            phone TEXT,
            npub TEXT,
            weight TEXT,
            paid BOOLEAN DEFAULT false,
            shipped BOOLEAN DEFAULT false,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
