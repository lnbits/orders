window.PageOrdersPublic = {
  template: '#page-orders-public',
  data: function () {
    return {
      url: '',
      ordersId: '',
      publicPageData: {}
    }
  },
  methods: {
    async fetchPublicData() {
      try {
        const {data} = await LNbits.api.request(
          'GET',
          `/orders/api/v1/orders/${this.ordersId}/public`
        )
        this.publicPageData = data || {}
      } catch (error) {
        console.warn(error)
        LNbits.utils.notifyApiError(error)
      }
    },
    formatBalance(amountMsat) {
      return LNbits.utils.formatBalance((amountMsat || 0) / 1000)
    }
  },
  created: async function () {
    this.ordersId = this.$route.params.id
    this.url =
      window.location.origin + '/orders/' + this.ordersId
    await this.fetchPublicData()
  }
}
