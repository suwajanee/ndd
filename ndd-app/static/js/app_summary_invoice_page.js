var summary_invoice = new Vue( {
    
    el: '.summary-invoice',
    data: {
        year: '',
        month: '',
        week: '',
        customer: '',
        sub_customer: '',
        summary_customer: '',
        summary_week: {},
        query: {},

        // test: '2222',

        customer_details: {},
        invoices: [],
        drayage_total: 0,
        gate_total: 0,

        mode: 'table',
        invoice_details: false,

        
    },

    methods: {
        reload(year, month, week, customer, sub_customer, summary_customer) {
            this.year = this.query.year = year
            this.month = month
            this.week = this.query.week = week

            this.customer = this.query.customer = customer

            if(sub_customer) {
                this.sub_customer = this.query.sub_customer = sub_customer
            }
            if(summary_customer) {
                this.summary_customer = this.query.summary_customer = summary_customer
            }

            summary_invoice_details.query = this.query

            this.getInvoice()
        },
        resetValue(){
            this.drayage_total = 0
            this.gate_total = 0
        },
        getInvoice() {
            this.resetValue()
            api("/summary/api/get-invoice/", "POST", this.query).then((data) => {
                this.customer_details = data.summary_customer
                this.summary_week = data.week
                summary_invoice_details.diesel_rate = this.summary_week.diesel_rate
                summary_invoice_details.summary_week_id = this.summary_week.id

                summary_invoice_details.customer_main = this.customer_details.customer_main
                if('customer_custom' in this.customer_details){
                    summary_invoice_details.customer_custom = this.customer_details.customer_custom
                    summary_invoice_details.customer_main = this.customer_details.customer_custom.customer
                }                 

                    
                this.invoices = data.invoice
                summary_invoice_details.getWorkList()
                this.totalCalc()
            })
        },

        totalCalc(){
            for(inv in this.invoices){
                var drayage = parseFloat(this.invoices[inv].drayage_total)
                var gate = parseFloat(this.invoices[inv].gate_total)

                if(! this.invoices[inv].detail.remark) {
                    this.invoices[inv].detail.remark = ''
                }

                if(isNaN(drayage)){
                    drayage = 0
                }
                if(isNaN(gate)){
                    gate = 0
                }

                this.drayage_total += drayage
                this.gate_total += gate
            }
        },

        changeStatus() {
            api("/summary/api/summary-customer-status/", "POST", {id: this.customer_details.id, status: this.customer_details.status}).then((data) => {
                this.getInvoice()
            })
        },

        changeInvoiceStatus(invoice) {
            api("/summary/api/invoice-status/", "POST", {id: invoice.id, status: invoice.status}).then((data) => {
                this.getInvoice()
            })
        },

        editInvoiceRemark() {
            api("/summary/api/edit-invoice-remark/", "POST", {invoice_remark: this.invoices}).then((data) => {
                this.getInvoice()
            })
            this.mode = 'table'
        },

        selectInvoice(id, invoice) {
            summary_invoice_details.invoice_details = true
            // if(id && invoice) {
            summary_invoice_details.reload(id, invoice)
            // }
        },
        

    }
})
