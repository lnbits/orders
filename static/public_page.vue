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
          <div class="text-subtitle2 q-mb-xs">Payment Hash</div>
          <div class="text-caption" v-text="publicPageData.payment_hash"></div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Amount</div>
          <div class="text-caption" v-text="formatBalance(publicPageData.amount_msat)"></div>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <div class="text-subtitle2 q-mb-xs">Items</div>
          <q-list dense bordered separator v-if="publicPageData.items && publicPageData.items.length">
            <q-item v-for="(item, idx) in publicPageData.items" :key="idx">
              <q-item-section>
                <q-item-label v-text="item.title || item.id || 'Item'"></q-item-label>
                <q-item-label caption v-if="item.note" v-text="item.note"></q-item-label>
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
            <span v-text="publicPageData.tpos_name || publicPageData.source"></span>
          </h6>
          <p class="q-my-none">
            <span v-text="publicPageData.created_at"></span>
          </p>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>
