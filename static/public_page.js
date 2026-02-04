window.PageOrdersPublic = {
  template: '#page-orders-public',
  delimiters: ['${', '}'],
  data: function () {
    return {
      url: '',
      ordersId: '',
      publicPageData: {},
      isOwner: false,
      printMode: null,
      qrSrc: ''
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
    async checkOwner() {
      try {
        await LNbits.api.request('GET', '/api/v1/auth', null)
        this.isOwner = true
      } catch (error) {
        this.isOwner = false
      }
    },
    async printOrder() {
      this.printMode = 'order'
      await this.$nextTick()
      setTimeout(() => window.print(), 50)
    },
    async printLabel() {
      this.printMode = 'label'
      await this.$nextTick()
      await this.waitForLabelAssets()
      setTimeout(() => window.print(), 50)
    },
    async waitForLabelAssets() {
      await this.$nextTick()
      const img = document.querySelector('.label-qr')
      if (!img) return
      if (img.complete && img.naturalWidth > 0) return
      await new Promise(resolve => {
        const done = () => resolve()
        img.addEventListener('load', done, {once: true})
        img.addEventListener('error', done, {once: true})
        setTimeout(done, 500)
      })
    },
    formatBalance(amountMsat) {
      return LNbits.utils.formatBalance((amountMsat || 0) / 1000)
    },
    formatDate(value) {
      if (!value) return ''
      let normalized = String(value)
      if (normalized.includes('+00:00')) {
        normalized = normalized.replace('+00:00', 'Z')
      }
      normalized = normalized.replace(/(\\.\\d{3})\\d+/, '$1')
      const parsed = new Date(normalized)
      if (Number.isNaN(parsed.getTime())) return value
      return LNbits.utils.formatDate(parsed.toISOString())
    }
  },
  created: async function () {
    this.ordersId = this.$route.params.id
    this.url = window.location.origin + '/orders/' + this.ordersId
    this.qrSrc = `${window.location.origin}/api/v1/qrcode?data=${encodeURIComponent(
      this.url
    )}`
    await this.fetchPublicData()
    await this.checkOwner()
    window.addEventListener('afterprint', () => {
      this.printMode = null
    })
  }
}
