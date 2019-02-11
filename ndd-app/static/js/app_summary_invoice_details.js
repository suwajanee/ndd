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
        container_color: {},
        // customer_details: {},
        // invoices: [],
        // drayage_total: 0,
        // gate_total: 0,

        work_list_modal_mode: 'create',
        filter_work: '',
        work_list: [],
        work_selected: [],

        table_edit: false,
        invoice_details: false,

        invoice_data: {
            invoice_no: '',
            customer_name: '',
            date_from: '',
            other: '',
        },
        

        saving: false,
        not_save: false,

        drayage_total: '',
        gate_total: '',
        
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

            })  
        },

        drayageTotal() {
            this.not_save = false
            var total = 0
            for(detail_index in this.invoice_detail_list) {
                var drayage_charge = this.invoice_detail_list[detail_index].drayage_charge
                var drayage = drayage_charge.drayage = drayage_charge.drayage.replace(',', '')   

                if(drayage_charge.other) {
                    for(other_index in drayage_charge.other) {
                        var other = drayage_charge.other[other_index].other_charge = drayage_charge.other[other_index].other_charge.replace(',', '')


                        try {

                            var other_result = eval(other)
                        }
                        catch(err) {
                            var other_result = 0
                            this.not_save = true
                        }
                        if(isNaN(other_result)){
                            other_result = 0
                        }
                        total += other_result
                    }
                }

                try {
                    var result = eval(drayage)
                }
                catch(err) {
                    var result = 0
                    this.not_save = true
                }
                if(isNaN(result)){
                    result = 0
                }

                total += result


            }

            this.drayage_total = total
            return total
        },
        gateTotal() {
            this.not_save = false
            var total = 0
            for(detail_index in this.invoice_detail_list) {
                var gate = this.invoice_detail_list[detail_index].gate_charge.gate = this.invoice_detail_list[detail_index].gate_charge.gate.replace(',', '')
                try {
                    var result = eval(gate)
                }
                catch(err) {
                    var result = 0
                    this.not_save = true
                }
                if(isNaN(result)){
                    result = 0
                }
                total += result
            }
            this.gate_total = total
            return total
        }

        
    },

    methods: {
        reload(invoice) {
            this.work_selected = []
            this.booking_field = booking_field_text
            this.container_color = container_color
            
            this.invoice = invoice
            this.invoice_id = invoice.id
            this.invoiceEditFields()
            this.getInvoiceDetails(this.invoice_id)
            this.getFormDefault()
            this.getYears()
            
        },

        // Get initial data
        getInvoiceDetails(invoice_id) {
            api("/summary/api/get-invoice-details/", "POST", {invoice_id: invoice_id}).then((data) => {
                this.afterGetInvoiceDetails(data) 
            })
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

        // Setup Data
        invoiceEditFields() {
            if(this.invoice.detail) {
                this.invoice_data.invoice_no = this.invoice.invoice_no
                this.invoice_data.customer_name = this.invoice.detail.customer_name
                this.invoice_data.date_from = this.invoice.detail.date_from
                this.invoice_data.other = this.invoice.detail.other
            }
        },

        addWorkKey() {
            if(this.customer_type == 'agent-transport') {
                for(inv_detail in this.invoice_detail_list){
                    var detail = this.invoice_detail_list[inv_detail]
                    detail.work = detail.work_agent_transport
                    // this.invoice_detail_list[inv_detail].work = Object.assign({}, this.invoice_detail_list[inv_detail].work_agent_transport)
                    if(! detail.drayage_charge.drayage) {
                        detail.drayage_charge.drayage = detail.work.price
                    }

                    // if('other' in detail.drayage_charge){
                    //     this.$set(detail, 'other_status', true)
                    // }
                    // else {
                    //     this.$set(detail, 'other_status', false)
                    // }

                }
            }
            else {
                for(inv_detail in this.invoice_detail_list){
                    var detail = this.invoice_detail_list[inv_detail]

                    detail.work = detail.work_normal

                    // if('other' in detail.drayage_charge){
                    //     this.$set(detail, 'other_status', true)
                    // }
                    // else {
                    //     this.$set(detail, 'other_status', false)
                    // }


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

        afterGetInvoiceDetails(data) {
            this.invoice_detail_list = data
            this.addWorkKey()
            this.work_selected = []
        },


        // Invoice 

        addNewInvoice() {
            var data = this.dataAddSummaryCustomer()

            api("/summary/api/add-invoice/", "POST", {summary_details: data}).then((data) => {
                if(data) {
                    this.query.summary_customer = data.customer_week.id
                    if(this.customer_custom.option == 'evergreen') {
                        this.addInvoiceDetailsEvergreen(data)
                    }
                    else {
                        this.addInvoiceDetails(data)    
                    }
                    this.reload(data)
                }
            })
        },

        editInvoiceWeek() {
            if(this.summary_week_id != this.invoice.customer_week.week.id) {
                var data = this.dataAddSummaryCustomer()
                data.week = this.invoice.customer_week.week.id
                api("/summary/api/edit-invoice-week/", "POST", {invoice_id: this.invoice_id, summary_details: data}).then((data) => {
                    if(data) {
                        summary_invoice.getInvoice()
                        $('#modalInvoiceDetails').modal('hide')
                        this.invoice_details = false
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
                        $('#modalInvoiceDetails').modal('hide')
                        this.invoice_details = false

                        if(summary_invoice.invoices.length-1 == 0) {
                            delete this.query.summary_customer
                        }
                    }
                })
            }
        },


        // Invoice Detail
        
        addInvoiceDetails(invoice) {
            summary_invoice.getInvoice()
            api("/summary/api/add-invoice-details/", "POST", {invoice_id: invoice.id, work_list: this.work_selected, customer_type: this.customer_type}).then((data) => {
                // this.reload(invoice)
                this.invoice_details = true
                this.afterGetInvoiceDetails(data) 
            })
            $('#modalWorkList').modal('hide');

        },

        editInvoiceDetails() {
            this.saving = true
            var post_data = {
                invoice_id: this.invoice_id, 
                invoice_data: this.invoice_data, 
                invoice_detail_list: this.invoice_detail_list, 
                customer_type: this.customer_type,
                drayage_total: this.drayage_total,
                gate_total: this.gate_total,

            }
            api("/summary/api/edit-invoice-details/", "POST", post_data).then((data) => {
                this.invoice_details = true
                summary_invoice.getInvoice()
                this.afterGetInvoiceDetails(data) 
                this.saving = false

            })

        },

        deleteInvoiceDetail(id, work_id) {
            if (confirm('Are you sure?')){
                var invoice_detail_id = [id]
                var drayage_total = this.drayage_total
                var gate_total = this.gate_total

                var invoice_details = this.invoice_detail_list.filter(x => {
                        if(work_id) {
                            return x.work.id == work_id
                        }
                        else {
                            return x.id == id
                        }
                    }
                )
                for(detail_index in invoice_details) {
                    var detail = invoice_details[detail_index]
                    var drayage_charge = detail.drayage_charge

                    drayage_total = eval(drayage_total - eval(drayage_charge.drayage))
                    if(drayage_charge.other) {
                        for(other_index in drayage_charge.other) {
                            drayage_total = eval(drayage_total - eval(drayage_charge.other[other_index].other_charge))
                        }
                    }
                    if(detail.gate_charge) {
                        gate_total = eval(gate_total - eval(detail.gate_charge.gate))
                    }
                }
       
                var post_data = {
                    invoice_id: this.invoice_id,
                    invoice_detail_id: invoice_detail_id,
                    customer_type: this.customer_type,
                    work_id: work_id,

                    drayage_total: drayage_total,
                    gate_total: gate_total,
                }
                api("/summary/api/delete-invoice-detail/", "POST", post_data).then((data) => {
                    if(data) {
                        summary_invoice.getInvoice()
                        this.afterGetInvoiceDetails(data)
                    }
                })
            }
        },

        addOtherCharge(id) {
            var detail_index = this.invoice_detail_list.findIndex(x => x.id == id)

            var drayage_charge = this.invoice_detail_list[detail_index].drayage_charge


            if(! drayage_charge.other) {
                this.$set(drayage_charge, 'other', [])
            }
            drayage_charge.other.push({'other_charge': '', 'other_remark': ''})
        },

        removeOtherCharge(id, index) {
            var detail_index = this.invoice_detail_list.findIndex(x => x.id == id)
            var other_charge = this.invoice_detail_list[detail_index].drayage_charge.other

            other_charge.splice(index,1)

        },

        checkContainer(id, color, index) {
            if(! color) {
                color = 1
            }
            else {
                color = (color + 1) % 4
                if(color==0) { color = '' }
            }

            api("/summary/api/check-container/", "POST", {invoice_id: this.invoice_id, invoice_detail_id: id, color: color, index: index}).then((data) => {

                var invoice_detail = this.invoice_detail_list.find(x => x.id == id)

                this.$set(invoice_detail.detail, 'color'+index, data)


            })
        },




        // Evergreen

        addInvoiceDetailsEvergreen(invoice) {
            summary_invoice.getInvoice()
            api("/summary/api/add-invoice-details-evergreen/", "POST", {invoice_id: invoice.id, work_list: this.work_selected}).then((data) => {
                // this.reload(invoice)
                this.invoice_details = true
                this.afterGetInvoiceDetails(data) 
            })
            $('#modalWorkList').modal('hide');

        },


        evergreenSelectWork(work_click, work_action) {
            var action = this.work_selected.indexOf(work_action)
            if(this.work_selected.indexOf(work_click) >= 0){
                this.work_selected.splice(action, 1)                
            }
            else {
                this.work_selected.push(work_click)
                this.work_selected.push(work_action)
            }
                
        },

        

    }
})
