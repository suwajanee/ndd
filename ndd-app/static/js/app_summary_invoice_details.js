var summary_invoice_details = new Vue( {
    
    el: '#summary-invoice-details',
    data: {
        // year: '',
        // month: '',
        // week: '',
        // customer: '',
        // sub_customer: '',
        query: {},
        invoice: {},
        invoice_id: '',
        summary_week_id: '',
        invoice_detail_list: [],

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
        work_list: [],
        work_selected: [],

        mode: 'table',
        invoice_details: false,

        invoice_customer_name: '',
        invoice_date_from: '',
        invoice_other_data: '',

        invoice_details_item: 0,

        
    },
    computed: {
        filteredWork() {
            if(this.filter_work === '') return this.work_list
            var lower_filter = this.filter_work.toLowerCase()
            return this.work_list.filter(work_list => {
                if(this.customer_type == 'normal'){
                    if(work_list.shipper) {
                        return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.shipper.name.toLowerCase().includes(lower_filter) 
                        || work_list.container_no.toLowerCase().includes(lower_filter)
                    }
                    else {
                        return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.container_no.toLowerCase().includes(lower_filter)
                    }
                }
                else {
                    if(work_list.shipper) {
                        return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.shipper.name.toLowerCase().includes(lower_filter) ||
                        work_list.container_1.toLowerCase().includes(lower_filter) || work_list.container_2.toLowerCase().includes(lower_filter)
                    }
                    else {
                        return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.container_1.toLowerCase().includes(lower_filter) || 
                        work_list.container_2.toLowerCase().includes(lower_filter)
                    }
                }
                // if(work_list.shipper && work_list.container_no) {
                //     return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.shipper.name.toLowerCase().includes(lower_filter) 
                //     || work_list.container_no.toLowerCase().includes(lower_filter)
                // }
                // else if(work_list.shipper && work_list.container_1 && work_list.container_2) {
                //     return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.shipper.name.toLowerCase().includes(lower_filter) ||
                //     work_list.container_1.toLowerCase().includes(lower_filter) || work_list.container_2.toLowerCase().includes(lower_filter)
                // }
                // else if(work_list.container_no) {
                //     return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.container_no.toLowerCase().includes(lower_filter)
                // }
                // else {
                //     return work_list.booking_no.toLowerCase().includes(lower_filter) || work_list.container_1.toLowerCase().includes(lower_filter) || 
                //     work_list.container_2.toLowerCase().includes(lower_filter)
                // }
            })  
        },

        
    },

    methods: {
        reload(invoice) {
            this.work_selected = []
            this.booking_field = booking_field_text

            this.invoice = invoice
            this.invoice_id = invoice.id
            this.invoiceEditFields()
            this.getInvoiceDetails(this.invoice_id)
            this.getFormDefault()
            this.getYears()
            
        },
        invoiceEditFields() {
            if(this.invoice.detail) {
                this.invoice_customer_name = this.invoice.detail.customer_name
                this.invoice_date_from = this.invoice.detail.invoice_date_from
                this.invoice_other_data = this.invoice.detail.other_data
            }
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
            api("/summary/api/get-summary-weeks-by-year/", "POST", {year: this.invoice.customer_week.week.year.year_label }).then((data) => {
                this.week_list = data
            })
        },

        getWorkList() {
            this.customer_type = this.customer_main.work_type
            if(this.customer_type == 'agent-transport') {
                api("/agent-transport/api/get-work-list/", "POST", this.query).then((data) => {
                    this.work_list = data
                })
            }
            else {
                api("/booking/api/get-work-list/", "POST", this.query).then((data) => {
                    this.work_list = data
                })
            }
        },

        getInvoiceDetails(invoice_id) {
            api("/summary/api/get-invoice-details/", "POST", {invoice_id: invoice_id}).then((data) => {
                this.invoice_detail_list = data
                this.addWorkKey()
            })
        },
        addWorkKey() {
            if(this.customer_type == 'agent-transport') {
                for(inv_detail in this.invoice_detail_list){
                    this.invoice_detail_list[inv_detail].work = this.invoice_detail_list[inv_detail].work_agent_transport
                    this.invoice_detail_list[inv_detail].drayage_charge.drayage = this.invoice_detail_list[inv_detail].work.price

                    if(! this.invoice_detail_list[inv_detail].detail.remark) {
                        this.invoice_detail_list[inv_detail].detail.remark = ''
                    }
                    if(! this.invoice_detail_list[inv_detail].detail.remark) {
                        this.invoice_detail_list[inv_detail].detail.remark = ''
                    }

                }
            }
            else {
                for(inv_detail in this.invoice_detail_list){
                    this.invoice_detail_list[inv_detail].work = this.invoice_detail_list[inv_detail].work_normal

                    if(! this.invoice_detail_list[inv_detail].detail.remark) {
                        this.invoice_detail_list[inv_detail].detail.remark = ''
                    }
                }
                
            }
        },



        dataAddSummaryCustomer() {
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
            return data
        },

        addNewInvoice() { 
            var data = this.dataAddSummaryCustomer()
            
            api("/summary/api/add-invoice/", "POST", {summary_details: data}).then((data) => {
                if(data) {
                    this.query.summary_customer = data.customer_week.id
                    summary_invoice.getInvoice()
                    this.addInvoiceDetails(data)
                }
            })
        },
        addInvoiceDetails(invoice) {
            api("/summary/api/add-invoice-details/", "POST", {invoice_id: invoice.id, work_list: this.work_selected, customer_type: this.customer_type}).then((data) => {
                this.reload(invoice)
                this.invoice_details = true
            })
            $('#modalWorkList').modal('hide');

        },

        editInvoiceWeek() {
            if(this.summary_week_id != this.invoice.customer_week.week.id) {
                var data = this.dataAddSummaryCustomer()
                data.week = this.invoice.customer_week.week.id
                api("/summary/api/edit-invoice-week/", "POST", {invoice_id: this.invoice_id, summary_details: data}).then((data) => {
                    if(data) {
                        summary_invoice.getInvoice()
                        $('#modalInvoiceDetails').modal('hide');
                        this.invoice_details = false
                        // this.reload(this.query)
                    }
                })
            }
            $('#modalInvoiceDetails').modal('hide');
        },

        deleteInvoice() {
            if (confirm('Are you sure?')){
                api("/summary/api/delete-invoice-week/", "POST", {invoice_id: this.invoice_id, summary_customer_id: this.query.summary_customer, customer_type: this.customer_type}).then((data) => {
                    if(data) {
                        summary_invoice.getInvoice()
                        $('#modalInvoiceDetails').modal('hide');
                        this.invoice_details = false
                    }
                })
            }
        },

        deleteInvoiceDetail(id) {
            if (confirm('Are you sure?')){
                var invoice_detail_id = [id]
                api("/summary/api/delete-invoice-detail/", "POST", {invoice_detail_id: invoice_detail_id, customer_type: this.customer_type}).then((data) => {
                    if(data) {
                        this.getInvoiceDetails(this.invoice_id)
                        this.getWorkList()
                    }
                })
            }
        },

        invoiceItem() {
            this.invoice_details_item += 1
            return this.invoice_details_item
        },

        evergreenSelectWork(work_click, work_action) {
            var action = this.work_selected.indexOf(work_action)
            if(this.work_selected.indexOf(work_click) >= 0){
                this.work_selected.splice(action, 1)
                
            }
            else {
                this.work_selected.push(work_action)
            }
            
        }

        
    }
})
