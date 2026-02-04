<template id="page-orders">
  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-8 col-lg-7 q-gutter-y-md">
      <q-card id="settingsCard">
        <q-card-section class="">
          <div class="row">
            <div class="col">
              <span class="text-h5">Orders</span>
              <q-btn
                @click="showSettingsDataForm()"
                v-if="true"
                unelevated
                split
                color="primary"
                icon="settings"
                class="float-right"
              >
              </q-btn>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <div class="q-mt-lg">
        <span class="text-h5">Orders</span>
      </div>
      <q-card id="ordersCard" class="q-mt-xs">
        <q-card-section class="">
          <div class="row items-center no-wrap q-mb-md">
            <div class="col">
              <q-input
                :label="$t('search')"
                dense
                class="q-pr-xl"
                v-model="ordersTable.search"
              >
                <template v-slot:before>
                  <q-icon name="search"> </q-icon>
                </template>
                <template v-slot:append>
                  <q-icon
                    v-if="ordersTable.search !== ''"
                    name="close"
                    @click="ordersTable.search = ''"
                    class="cursor-pointer"
                  >
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-auto">
              <q-btn
                flat
                color="grey"
                icon="file_download"
                @click="exportOrdersCSV"
                >CSV</q-btn
              >
            </div>
          </div>
          <q-table
            dense
            flat
            :rows="ordersList"
            row-key="id"
            :columns="ordersTable.columns"
            v-model:pagination="ordersTable.pagination"
            :loading="ordersTable.loading"
            @request="getOrders"
          >
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th auto-width></q-th>
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                  ${ col.label }
                </q-th>
              </q-tr>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td auto-width>
                  <q-btn
                    flat
                    dense
                    size="xs"
                    icon="launch"
                    color="primary"
                    type="a"
                    :href="'/orders/' + props.row.id"
                    target="_blank"
                    class="q-mr-sm"
                    ><q-tooltip>Open public page</q-tooltip></q-btn
                  >

                  <q-btn
                    flat
                    dense
                    size="xs"
                    @click="deleteOrders(props.row.id)"
                    icon="cancel"
                    color="pink"
                    class="q-mr-sm"
                  >
                    <q-tooltip> Delete </q-tooltip>
                  </q-btn>
                </q-td>

                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <div v-if="col.field == 'amount_msat'">
                    <span v-text="formatBalance(col.value)"></span>
                  </div>
                  <div v-else-if="col.field == 'created_at'">
                    <span v-text="dateFromNow(col.value)"> </span>
                  </div>
                  <div v-else>${ col.value }</div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>

    <div class="col-12 col-md-4 col-lg-5 q-gutter-y-md">
      <q-card>
        <q-card-section>
          <h6 class="text-subtitle1 q-my-none">Orders</h6>
          <p>If enabled orders from tpos and webshop will be pulled.</p>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <q-separator></q-separator>
          <q-list>
            <!-- {% include "orders/_api_docs.html" %} -->
            <q-separator></q-separator>
            <q-expansion-item group="extras" icon="info" label="More info">
              <q-card>
                <q-card-section>
                  <p>Some more info about Orders.</p>
                  <small
                    >Created by
                    <a
                      class="text-secondary"
                      href="https://github.com/lnbits"
                      target="_blank"
                      >LNbits extension builder</a
                    >.</small
                  >
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <!--/////////////////////////////////////////////////-->
    <!--//////////////FORM DIALOG////////////////////////-->
    <!--/////////////////////////////////////////////////-->

    <q-dialog v-model="settingsFormDialog.show" position="top">
      <q-card
        v-if="settingsFormDialog.show"
        class="q-pa-lg q-pt-xl lnbits__dialog-card q-col-gutter-md"
      >
        <span class="text-h5">Settings</span>

        <q-input
          filled
          dense
          v-model.trim="settingsFormDialog.data.npub"
          label="Nostr npub"
          hint="  (optional)"
        ></q-input>

        <q-input
          filled
          dense
          v-model.trim="settingsFormDialog.data.telegram"
          label="Telegram chat ID"
          hint="  (optional)"
        ></q-input>

        <q-input
          filled
          dense
          v-model.trim="settingsFormDialog.data.email"
          label="Email"
          hint="  (optional)"
        ></q-input>

        <div class="row q-mt-lg">
          <q-btn
            @click="updateSettings"
            unelevated
            color="primary"
            type="submit"
            >Update</q-btn
          >
          <q-btn v-close-popup flat color="grey" class="q-ml-auto"
            >Cancel</q-btn
          >
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>
