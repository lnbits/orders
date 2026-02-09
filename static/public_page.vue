<!--/////////////////////////////////////////////////-->
<!--////////////////USER FACING PAGE/////////////////-->
<!--/////////////////////////////////////////////////-->

<template id="page-orders-public">
  <div class="row q-col-gutter-md justify-center">
    <div class="col-12 col-sm-6 col-md-5 col-lg-4">
      <q-card class="q-pa-lg">
        <q-card-section class="q-pa-none q-mb-md">
          <span class="text-h5">Order</span>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <q-btn
            unelevated
            color="primary"
            icon="print"
            @click="printOrder"
            class="q-mr-sm"
            >Print Order</q-btn
          >
          <q-btn
            outline
            color="grey-8"
            icon="local_shipping"
            @click="printLabel"
            >Print Label</q-btn
          >
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Payment Hash</div>
          <div class="text-caption" v-text="publicPageData.payment_hash"></div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Amount</div>
          <div
            class="text-caption"
            v-text="formatBalance(publicPageData.amount_msat)"
          ></div>
          <div
            class="text-caption"
            v-if="publicPageData.fiat_amount && publicPageData.fiat_currency"
            v-text="
              formatFiatAmount(
                publicPageData.fiat_amount,
                publicPageData.fiat_currency
              )
            "
          ></div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Customer</div>
          <div
            class="text-caption"
            v-text="
              publicPageData.email ||
              publicPageData.phone ||
              publicPageData.npub ||
              '—'
            "
          ></div>
          <div
            class="text-caption"
            v-text="publicPageData.address || '—'"
          ></div>
          <div class="text-caption" v-if="publicPageData.weight">
            Weight: <span v-text="publicPageData.weight"></span>
          </div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Status</div>
          <div class="text-caption">
            <q-badge
              :color="publicPageData.paid ? 'green' : 'grey'"
              align="middle"
            >
              <span v-text="publicPageData.paid ? 'Paid' : 'Unpaid'"></span>
            </q-badge>
            <q-badge
              class="q-ml-sm"
              :color="publicPageData.shipped ? 'green' : 'orange'"
              align="middle"
            >
              <span
                v-text="publicPageData.shipped ? 'Shipped' : 'Not shipped'"
              ></span>
            </q-badge>
          </div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Items</div>
          <q-list
            dense
            bordered
            separator
            v-if="publicPageData.items && publicPageData.items.length"
          >
            <q-item v-for="(item, idx) in publicPageData.items" :key="idx">
              <q-item-section>
                <q-item-label
                  v-text="item.title || item.name || item.id || 'Item'"
                ></q-item-label>
                <q-item-label
                  caption
                  v-if="item.note"
                  v-text="item.note"
                ></q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label v-text="item.quantity || 1"></q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
          <div v-else class="text-caption">No line items</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-5 col-lg-4 q-gutter-y-md">
      <q-card>
        <q-card-section>
          <h6 class="q-mb-sm q-mt-none">
            <span
              v-text="publicPageData.tpos_name || publicPageData.source"
            ></span>
          </h6>
          <p class="q-my-none">
            <span v-text="formatDate(publicPageData.created_at)"></span>
          </p>
          <p class="q-my-none">
            <span v-text="publicPageData.business_name"></span>
          </p>
          <p class="q-my-none">
            <span v-text="publicPageData.business_address"></span>
          </p>
        </q-card-section>
      </q-card>
    </div>
  </div>

  <Teleport to="body">
    <div class="receipt" :class="printMode" v-if="printMode">
      <template v-if="printMode === 'label'">
        <div class="label-card">
          <div class="label-section" v-if="publicPageData.address">
            <div class="label-row">
              <div class="label-badge">Ship to</div>
              <div class="label-address" v-text="publicPageData.address"></div>
            </div>
          </div>
          <div
            class="label-section"
            v-if="
              publicPageData.business_name || publicPageData.business_address
            "
          >
            <div class="label-row">
              <div class="label-title">From</div>
              <div>
                <div
                  class="label-address"
                  v-text="publicPageData.business_name || '—'"
                ></div>
                <div
                  class="label-address label-address-muted"
                  v-if="publicPageData.business_address"
                  v-text="publicPageData.business_address"
                ></div>
              </div>
            </div>
          </div>
          <div class="label-section">
            <div class="label-grid">
              <div class="label-field">
                <div class="label-field-title">Order ID</div>
                <div class="label-field-value" v-text="publicPageData.id"></div>
              </div>
              <div class="label-field" v-if="publicPageData.weight">
                <div class="label-field-title">Weight</div>
                <div
                  class="label-field-value"
                  v-text="publicPageData.weight"
                ></div>
              </div>
              <div class="label-field">
                <div class="label-field-title">Shipping date</div>
                <div
                  class="label-field-value"
                  v-text="formatDate(publicPageData.created_at)"
                ></div>
              </div>
            </div>
          </div>
          <div class="label-section label-barcode">
            <img class="label-qr" :src="qrSrc" alt="Order QR" v-if="qrSrc" />
            <div class="barcode-text">Scan for order</div>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="print-header">
          <div
            class="print-business-name"
            v-text="publicPageData.business_name"
          ></div>
          <div
            class="print-return-label"
            v-if="publicPageData.business_address"
          >
            Return address
          </div>
          <div
            class="print-business-address"
            v-text="publicPageData.business_address"
          ></div>
        </div>

        <div class="print-section" v-if="publicPageData.address">
          <div class="print-address-badge">Shipping address</div>
          <div
            class="print-value print-address"
            v-text="publicPageData.address"
          ></div>
        </div>

        <div class="print-section">
          <div class="print-label">Order</div>
          <div class="print-value" v-text="publicPageData.id"></div>
          <div class="print-value" v-if="printMode === 'order'">
            Amount:
            <span v-text="formatBalance(publicPageData.amount_msat)"></span>
          </div>
          <div
            class="print-value"
            v-if="
              printMode === 'order' &&
              publicPageData.fiat_amount &&
              publicPageData.fiat_currency
            "
          >
            Fiat amount:
            <span
              v-text="
                formatFiatAmount(
                  publicPageData.fiat_amount,
                  publicPageData.fiat_currency
                )
              "
            ></span>
          </div>
          <div
            class="print-value"
            v-text="formatDate(publicPageData.created_at)"
          ></div>
        </div>

        <div
          class="print-section"
          v-if="
            printMode === 'order' &&
            publicPageData.items &&
            publicPageData.items.length
          "
        >
          <div class="print-label">Items</div>
          <table class="print-items">
            <thead>
              <tr>
                <th>Item</th>
                <th class="qty">Qty</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in publicPageData.items" :key="idx">
                <td v-text="item.title || item.name || item.id || 'Item'"></td>
                <td class="qty" v-text="item.quantity || 1"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </Teleport>
</template>

<style>
.receipt {
  display: none;
}
@media screen {
  .receipt {
    display: none;
  }
}
@media print {
  @page {
    size: auto;
    margin: 0;
  }
  html {
    font-size: 12px !important;
  }
  * {
    color: black !important;
    background: white !important;
  }
  body > * {
    display: none !important;
  }
  .receipt {
    display: block !important;
    margin: 0mm !important;
    padding: 16px !important;
    font-family: Arial, sans-serif;
    color: #111;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .print-header {
    text-align: center;
    margin-bottom: 12px;
  }
  .print-business-name {
    font-size: 18px;
    font-weight: 700;
  }
  .print-business-address {
    font-size: 10px;
    white-space: pre-line;
  }
  .print-return-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #555;
    margin-bottom: 4px;
  }
  .print-address-badge {
    display: inline-block;
    padding: 2px 8px;
    background: #000;
    color: #fff;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
  }
  .print-address {
    font-size: 15px;
    font-weight: 600;
  }
  .print-section {
    margin-bottom: 12px;
  }
  .print-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #555;
  }
  .print-value {
    font-size: 14px;
    margin-top: 4px;
    white-space: pre-line;
  }
  .print-items {
    width: 100%;
    border-collapse: collapse;
  }
  .print-items th,
  .print-items td {
    border-bottom: 1px solid #ddd;
    padding: 6px 0;
    font-size: 12px;
    text-align: left;
  }
  .print-items th.qty,
  .print-items td.qty {
    text-align: right;
    width: 60px;
  }
  .label-card {
    border: 2px solid #000;
    border-radius: 12px;
    padding: 12px;
  }
  .label-section {
    border-top: 2px solid #000;
    padding: 12px 4px;
  }
  .label-section:first-of-type {
    border-top: none;
    padding-top: 4px;
  }
  .label-row {
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }
  .label-badge {
    background: #000 !important;
    color: #fff !important;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    white-space: nowrap;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .label-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
    color: #222;
    min-width: 70px;
  }
  .label-address {
    font-size: 13px;
    font-weight: 600;
    white-space: pre-line;
  }
  .label-address-muted {
    font-weight: 500;
    margin-top: 4px;
  }
  .label-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px 20px;
  }
  .label-field-title {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #333;
    font-weight: 700;
  }
  .label-field-value {
    font-size: 12px;
    margin-top: 4px;
    font-weight: 600;
    word-break: break-word;
  }
  .label-barcode {
    text-align: center;
  }
  .barcode-placeholder {
    height: 70px;
    border: 2px dashed #000;
    margin: 6px auto 8px;
  }
  .label-qr {
    width: 160px;
    height: 160px;
    display: block;
    margin: 0 auto 8px;
    object-fit: contain;
  }
  .barcode-text {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
}
</style>
