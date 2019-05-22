var summary_invoice_details = new Vue( {
    
    el: '#summary-invoice-details',
    data: {
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

        container_size_1: [],
        container_size_2: [],

        customer_form: [],
        form_default: [],
        booking_field: {},
        diesel_rate: '',
        container_color: {},

        work_list_modal_mode: 'create',
        filter_work: '',
        work_list: [],
        work_selected: [],
        filtered_work: [],
        selected_all: false,

        table_edit: false,
        invoice_details: false,

        invoice_data: {
            invoice_no: '',
            customer_name: '',
            date_from: '',
            other: '',
            order_by_remark: '',
        },
        
        saving: false,
        not_save: false,

        drayage_total: '',
        gate_total: '',
    },
    computed: {
        filteredWork() {
            if(this.filter_work === '') {
                this.filtered_work = this.work_list
                return this.work_list
            }
            var lower_filter = this.filter_work.trim().toLowerCase()
            this.filtered_work = this.work_list.filter(work_list => {
                if(this.customer_type == 'normal'){
                    if(work_list.shipper) {
                        return work_list.booking_no.trim().toLowerCase().includes(lower_filter) || work_list.shipper.name.trim().toLowerCase().includes(lower_filter) 
                        || work_list.container_no.trim().toLowerCase().includes(lower_filter)
                    }
                    else {
                        return work_list.booking_no.trim().toLowerCase().includes(lower_filter) || work_list.container_no.trim().toLowerCase().includes(lower_filter)
                    }
                }
                else {
                    if(work_list.shipper) {
                        return work_list.booking_no.trim().toLowerCase().includes(lower_filter) || work_list.shipper.name.trim().toLowerCase().includes(lower_filter) ||
                        work_list.container_1.trim().toLowerCase().includes(lower_filter) || work_list.container_2.trim().toLowerCase().includes(lower_filter)
                    }
                    else {
                        return work_list.booking_no.trim().toLowerCase().includes(lower_filter) || work_list.container_1.trim().toLowerCase().includes(lower_filter) || 
                        work_list.container_2.trim().toLowerCase().includes(lower_filter)
                    }
                }
            })
            return this.filtered_work
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

            this.drayage_total = parseFloat(total.toFixed(2))
            return this.drayage_total
        },

        gateTotal() {
            this.not_save = false
            var total = 0
            for(detail_index in this.invoice_detail_list) {
                var gate_charge = this.invoice_detail_list[detail_index].gate_charge
                var gate = gate_charge.gate = gate_charge.gate.replace(',', '')
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

                if('vat' in gate_charge) {
                    var vat = gate_charge.vat = gate_charge.vat.replace(',', '')
                    try {
                        var result_vat = eval(vat)
                    }
                    catch(err) {
                        var result_vat = 0
                        this.not_save = true
                    }
                    if(isNaN(result_vat)){
                        result_vat = 0
                    }
                    total += result_vat
                }
            }

            this.gate_total = parseFloat(total.toFixed(2))
            return this.gate_total
        }
    },

    methods: {
        reload(invoice) {
            this.work_selected = []
            this.booking_field = booking_field_text
            this.container_color = container_color
            
            this.invoice = invoice

            this.invoice_id = invoice.id

            this.getContainerSize()
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
            api("/summary/api/get-summary-weeks-by-year/", "POST", { year: this.invoice.customer_week.week.year.year_label }).then((data) => {
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
        getContainerSize() {
            api("/booking/api/get-container-size/").then((data) => {
                this.container_size_1 = data.num_1
                this.container_size_2 = data.num_2
            })
        },

        // Setup Data
        invoiceEditFields() {
            if(this.invoice.detail) {
                this.invoice_data.customer_name = this.invoice.detail.customer_name
                this.invoice_data.date_from = this.invoice.detail.date_from
                this.invoice_data.other = this.invoice.detail.other
                this.invoice_data.order_by_remark = this.invoice.detail.order_by_remark || false
            }
        },

        afterGetInvoiceDetails(data) {
            this.invoice_data.invoice_no = this.invoice.invoice_no.split(',')
            this.invoice_detail_list = data
            this.addWorkKey()
            this.work_selected = []
        },

        addWorkKey() {
            if(this.customer_type == 'agent-transport') {
                this.invoice_detail_list.forEach(function(inv_detail) {
                    inv_detail.work = inv_detail.work_agent_transport
                    if(! inv_detail.drayage_charge.drayage) {
                        inv_detail.drayage_charge.drayage = inv_detail.work.price
                    }
                })
            }
            else {
                this.invoice_detail_list.forEach(function(inv_detail) {
                    inv_detail.work = inv_detail.work_normal
                })
            }
        },

        addTimeRemark() {
            this.invoice_detail_list.forEach(function(inv_detail) { 
                try {
                    var time = inv_detail.work.time.split('.')
                    if(! inv_detail.detail.remark && parseInt(time[0])==6) {
                        inv_detail.detail.remark = '**' + inv_detail.work.time + '**'
                    }
                }
                catch(err) {
                    inv_detail.detail.remark = ''
                }
            })
            this.editInvoiceDetails()
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

        // Invoice 
        addNewInvoice() {
            var data = this.dataAddSummaryCustomer()

            api("/summary/api/add-invoice/", "POST", {summary_details: data}).then((data) => {
                if(data) {
                    this.invoice = data
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
        selectAllWork() {
            this.work_selected = []

            if (this.selected_all) {
                for (work in this.filtered_work) {
                    if (this.filtered_work[work].summary_status != '1') {
                        this.work_selected.push(this.filtered_work[work].id) 
                    }
                }
            }
        },
        selectWork(id, status) {
            if(status != '1') {
                var index = this.work_selected.indexOf(id);
                if(index > -1) {
                    this.work_selected.splice(index, 1);
                }
                else {
                    this.work_selected.push(id)
                }
            }
        },
        addInvoiceDetails(invoice) {
            summary_invoice.getInvoice()
            api("/summary/api/add-invoice-details/", "POST", {invoice_id: invoice.id, work_list: this.work_selected, customer_type: this.customer_type}).then((data) => {
                this.invoice_details = true
                this.afterGetInvoiceDetails(data)
                if(this.customer_custom.option == 'time_remark') {
                    this.addTimeRemark()
                }
                this.selected_all = false
            })
            $('#modalWorkList').modal('hide');
        },

        editInvoiceDetails() {
            this.saving = true

            this.invoice.invoice_no = this.invoice_data.invoice_no = this.invoice_data.invoice_no.toString()
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

                this.invoice.drayage_total = this.drayage_total
                this.invoice.gate_total = this.gate_total
                
                this.saving = false
            })
        },

        tryCatchTotal(val) {
            try {
                var result = eval(val)
            }
            catch(err) {
                var result = 0
            }
            if(isNaN(result)){
                result = 0
            }
            return result
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

                    var drayage = this.tryCatchTotal(drayage_charge.drayage)
                    drayage_total = eval(drayage_total - eval(drayage))

                    if(drayage_charge.other) {
                        for(other_index in drayage_charge.other) {
                            var other = this.tryCatchTotal(drayage_charge.other[other_index].other_charge)
                            drayage_total = eval(drayage_total - eval(other))
                        }
                    }
                    if(detail.gate_charge) {
                        var gate = this.tryCatchTotal(detail.gate_charge.gate)
                        gate_total = eval(gate_total - eval(gate))
                        
                        if(detail.gate_charge.vat) {
                            var vat = this.tryCatchTotal(detail.gate_charge.vat)
                            gate_total = eval(gate_total - eval(vat))
                        }
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
            drayage_charge.other.push({'other_charge': '', 'other_remark': '', 'color': 0})
        },

        textColorOtherCharge(id, index, color) {
            var detail_index = this.invoice_detail_list.findIndex(x => x.id == id)
            var other_charge = this.invoice_detail_list[detail_index].drayage_charge.other
            other_charge[index].color = color
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
                color = (color + 1) % 5
                if(color==0) { color = '' }
            }

            api("/summary/api/check-container/", "POST", {invoice_id: this.invoice_id, invoice_detail_id: id, color: color, index: index}).then((data) => {
                var invoice_detail = this.invoice_detail_list.find(x => x.id == id)
                this.$set(invoice_detail.detail, 'color' + index, data)
            })
        },

        copyToAll(value, key1, key2) {
            this.invoice_detail_list.forEach(function(inv_detail) {
                inv_detail[key1][key2] = value
            })
        },

        // Evergreen
        addInvoiceDetailsEvergreen(invoice) {
            summary_invoice.getInvoice()
            api("/summary/api/add-invoice-details-evergreen/", "POST", {invoice_id: invoice.id, work_list: this.work_selected}).then((data) => {
                this.invoice_details = true
                this.afterGetInvoiceDetails(data) 
            })
            $('#modalWorkList').modal('hide');
        },

        evergreenSelectWork(work_click, work_action, id, status) {
            if(status != '1') {
                if(this.work_selected.indexOf(work_click) >= 0){
                    var index_1 = this.work_selected.indexOf(id + '_1')
                    this.work_selected.splice(index_1, 1)
                    var index_2 = this.work_selected.indexOf(id + '_2')
                    this.work_selected.splice(index_2, 1)       
                }
                else {
                    this.work_selected.push(work_click)
                    this.work_selected.push(work_action)
                }
            }
        },

    }
})
