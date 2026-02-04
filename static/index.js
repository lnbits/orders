window.PageOrders = {
  template: '#page-orders',
  delimiters: ['${', '}'],
  data: function () {
    return {
      settingsFormDialog: {
        show: false,
        data: {}
      },

      ordersFormDialog: {
        show: false,
        data: {}
      },
      ordersList: [],
      ordersTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'source',
            align: 'left',
            label: 'Source',
            field: 'source',
            sortable: true
          },
          {
            name: 'tpos_name',
            align: 'left',
            label: 'TPoS',
            field: 'tpos_name',
            sortable: true
          },
          {
            name: 'amount_msat',
            align: 'left',
            label: 'Amount',
            field: 'amount_msat',
            sortable: true
          },
          {
            name: 'email',
            align: 'left',
            label: 'Email',
            field: 'email',
            sortable: true
          },
          {
            name: 'address',
            align: 'left',
            label: 'Address',
            field: 'address',
            sortable: true
          },
          {
            name: 'paid',
            align: 'left',
            label: 'Paid',
            field: 'paid',
            sortable: true
          },
          {
            name: 'shipped',
            align: 'left',
            label: 'Shipped',
            field: 'shipped',
            sortable: true
          },
          {
            name: 'payment_hash',
            align: 'left',
            label: 'Payment Hash',
            field: 'payment_hash',
            sortable: true
          },
          {
            name: 'created_at',
            align: 'left',
            label: 'Created',
            field: 'created_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'created_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      }
    }
  },
  watch: {
    'ordersTable.search': {
      handler() {
        const props = {}
        if (this.ordersTable.search) {
          props['search'] = this.ordersTable.search
        }
        this.getOrders()
      }
    }
  },

  methods: {
    //////////////// Settings ////////////////////////
    async updateSettings() {
      try {
        const data = {...this.settingsFormDialog.data}

        await LNbits.api.request('PUT', '/orders/api/v1/settings', null, data)
        this.settingsFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    async getSettings() {
      try {
        const {data} = await LNbits.api.request(
          'GET',
          '/orders/api/v1/settings',
          null
        )
        this.settingsFormDialog.data = data
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    async showSettingsDataForm() {
      await this.getSettings()
      this.settingsFormDialog.show = true
    },

    async getOrders(props) {
      try {
        this.ordersTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(this.ordersTable, props)
        const {data} = await LNbits.api.request(
          'GET',
          `/orders/api/v1/orders/paginated?${params}`,
          null
        )
        this.ordersList = data.data
        this.ordersTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.ordersTable.loading = false
      }
    },
    async deleteOrders(ordersId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Orders?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/orders/api/v1/orders/' + ordersId,
              null
            )
            await this.getOrders()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },
    async toggleShipped(row) {
      try {
        await LNbits.api.request(
          'PUT',
          `/orders/api/v1/orders/${row.id}/shipping`,
          null,
          {shipped: !row.shipped}
        )
        await this.getOrders()
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    async exportOrdersCSV() {
      await LNbits.utils.exportCSV(
        this.ordersTable.columns,
        this.ordersList,
        'orders_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow()
    },
    formatBalance(amountMsat) {
      return LNbits.utils.formatBalance(amountMsat / 1000)
    }
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.getOrders()
  }
}
