var summary_invoice = new Vue( {
    
    el: '#summary-invoice',
    data: {
        year: '',
        month: '',
        week: '',
        customer: '',
        sub_customer: '',
        summary_customer: '',
        summary_week: {},
        query: {},

        customer_details: {},
        invoices: [],
        drayage_total: 0,
        gate_total: 0,

        table_edit: false,
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
                if(this.customer_details.customer_custom != null){
                    summary_invoice_details.customer_custom = this.customer_details.customer_custom
                    summary_invoice_details.customer_main = this.customer_details.customer_custom.customer
                }                 

                this.invoices = data.invoice
                summary_invoice_details.getWorkList()
                this.totalCalc()
            })
        },
        totalCalc(){
            var drayage_total = 0
            var gate_total = 0
            if(this.invoices) {
                this.invoices.forEach(function(invoice) {
                    var drayage = parseFloat(invoice.drayage_total)
                    var gate = parseFloat(invoice.gate_total)

                    if(! invoice.detail.remark) {
                        invoice.detail.remark = ''
                    }

                    if(isNaN(drayage)){
                        drayage = 0
                    }
                    if(isNaN(gate)){
                        gate = 0
                    }

                    drayage_total += drayage
                    gate_total += gate
                })
            }
            this.drayage_total = drayage_total
            this.gate_total = gate_total

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
            this.table_edit = false
        },

        selectInvoice(invoice) {
            summary_invoice_details.invoice_details = true                
            summary_invoice_details.reload(invoice)
        },
        
    }
})
