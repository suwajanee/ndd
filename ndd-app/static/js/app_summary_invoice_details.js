var summary_invoice_details = new Vue( {
    
    el: '#summary-invoice-details',
    data: {
        // year: '',
        // month: '',
        // week: '',
        // customer: '',
        // sub_customer: '',
        query: {},
        invoice: '',
        invoice_id: '',
        summary_week_id: '',

        year_list: [],
        week_list: [],

        customer_custom: {},
        customer_main: {},
        customer_type: '',

        customer_form: [],
        form_default: [],
        booking_field: {},
        diesel_rate: '',
        // customer_details: {},
        // invoices: [],
        // drayage_total: 0,
        // gate_total: 0,

        filter_work: '',
        work_choices: [],
        work_selected: [],

        mode: 'table',
        invoice_details: false,

        
    },
    computed: {
        filteredWork() {
            if(this.filter_work === '') return this.work_choices
            return this.work_choices.filter(work_choices => {
                if(work_choices.shipper) {
                    return work_choices.booking_no.toLowerCase().includes(this.filter_work.toLowerCase()) || work_choices.shipper.name.toLowerCase().includes(this.filter_work.toLowerCase())
                }
                else {
                    return work_choices.booking_no.toLowerCase().includes(this.filter_work.toLowerCase())
                }
            })  
        }
    },

    methods: {
        reload(invoice) {
            this.booking_field = booking_field_text

            this.invoice = invoice.invoice_no
            this.invoice_id = invoice.id
            this.getFormDefault()
            this.getYears()
            
        },

        getFormDefault() {
            api("/summary/api/get-form-default/").then((data) => {
                this.form_default = data.form_detail
                if(! this.customer_custom){
                    this.customer_form = this.form_default
                }
                else if(! this.customer_custom.form){
                    this.customer_form = this.form_default
                }
                else {
                    this.customer_form = this.customer_custom.form.form_detail
                }
            })
        },
        getYears() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_list = data
                this.getWeeks()
            })
        },
        getWeeks() {
            api("/summary/api/get-summary-weeks-by-year/", "POST", {year: this.query.year }).then((data) => {
                this.week_list = data
            })
        },

        getWorkList() {
            this.customer_type = this.customer_main.work_type
            if(this.customer_type == 'agent-transport') {
                api("/agent-transport/api/get-work-list/", "POST", this.query).then((data) => {
                    this.work_choices = data
                })
            }
            else {
                api("/booking/api/get-work-list/", "POST", this.query).then((data) => {
                    this.work_choices = data
                })
            }
        },

        addNewInvoice() {
            var data = {
                week: this.summary_week_id,
                customer_main: this.query.customer,
            }
            if(this.query.sub_customer) {
                data.customer_custom = this.query.sub_customer
            }
            if(this.query.summary_customer) {
                data.summary_customer_id = this.query.summary_customer
            }
            
            api("/summary/api/add-invoice/", "POST", {summary_details: data}).then((data) => {
                if(data) {
                    this.query.summary_customer = data.customer_week.id
                    summary_invoice.getInvoice()
                    this.reload(data)
                }
            })

        }
        
    }
})
