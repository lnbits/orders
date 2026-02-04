<a href="https://lnbits.com" target="_blank" rel="noopener noreferrer">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/QE6SIrs.png">
    <img src="https://i.imgur.com/fyKPgVT.png" alt="LNbits" style="width:280px">
  </picture>
</a>

[![License: MIT](https://img.shields.io/badge/License-MIT-success?logo=open-source-initiative&logoColor=white)](./LICENSE)
[![Built for LNbits](https://img.shields.io/badge/Built%20for-LNbits-4D4DFF?logo=lightning&logoColor=white)](https://github.com/lnbits/lnbits)

# Orders — _[LNbits](https://lnbits.com) extension_

**Capture paid TPoS orders and keep them in one place.**  
Orders are pushed automatically when a TPoS invoice settles.

---

### Quick Links

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Notifications](#notifications)

## Overview

Orders stores a normalized copy of paid TPoS receipts (items, totals, and metadata).
Enable it for a user and every TPoS payment is recorded in the Orders list.

## Features

- **Auto-capture** — paid TPoS invoices become Orders
- **Items & totals** — stores line items, tax, and exchange rate data
- **Source tracking** — keeps TPoS id/name and payment hash
- **Notifications** — optional Telegram/Nostr/Email alerts

## Usage

1. **Enable** the Orders extension.
2. **Enable** TPoS (if not already enabled).
3. **Take a payment** in TPoS.
4. **Open Orders** to view the captured order.

## Notifications

Open **Orders → Settings** and configure one or more:

- Telegram chat ID
- Nostr npub
- Email address (comma separated)
