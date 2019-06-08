var summary_week_details = new Vue( {
    
    el: '#summary-week-details',
    data: {
        year: '',
        month: '',
        week: '',
        month_list: [],
        year_list: [],

        week_details: {},

        item: 0,

        summary_week_details: [],
        total_list: [],
        withholding_list: [],
        check_list: [],
        sum_total: [],

        input_required: false,
        modal_action: 'edit',
        summary_week_modal: {
            id: '',
            year: '',
            month: '',
            week: '',
            date_start: '',
            date_end: '',
            diesel_rate: '',
            status: '',
        },

        table_edit: false,
        saving: false,
        customer_note: [],
        edit_data: [],

        loading: false,
    },

    methods: {
        reload(year, month, week) {
            this.year = this.summary_week_modal.year = year
            this.month = this.summary_week_modal.month = month
            this.week = this.summary_week_modal.week = week
            this.month_list = _month
            this.getSummaryWeekDetails(year, month, week)
            this.getYears()
        },
        getYears() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_list = data
            })
        },
        resetValue(){
            this.item = 0
            this.total_list = []
            this.withholding_list = []
            this.check_list = []
            this.edit_data = []
        },
        getSummaryWeekDetails(year, month, week) {
            this.loading = true
            this.resetValue()
            api("/summary/api/get-summary-week-details/", "POST", { year: year, month: month, week: week }).then((data) => {
                if(data == 'Error'){
                    window.location.replace("/summary/" + this.year)
                    return false
                }
                this.summary_week_details = data.summary_week_details
                this.week_details = data.week
                this.summary_week_modal.id = this.week_details.id
                this.summary_week_modal.date_start = this.week_details.date_start
                this.summary_week_modal.date_end = this.week_details.date_end
                this.summary_week_modal.diesel_rate = this.week_details.diesel_rate
                this.summary_week_modal.status = this.week_details.status

                this.totalCalc()
                this.loading = false
            })
        },
        totalCalc() {
            var drayage_total = gate_total = 0
            for(week in this.summary_week_details) {
                var customer_data = {}

                var drayage = this.summary_week_details[week].drayage_total
                var gate = this.summary_week_details[week].gate_total

                customer_data.id = summary_id = this.summary_week_details[week].id

                if(summary_id) {
                    this.summary_week_details[week].item = ++this.item

                    customer_data.date_billing = this.summary_week_details[week].date_billing
                    customer_data.date_due = this.summary_week_details[week].date_due
                    customer_data.remark = this.summary_week_details[week].remark

                    this.customer_note.push(customer_data)

                }

                if(isNaN(drayage)){
                    drayage = 0
                }
                if(isNaN(gate)){
                    gate = 0
                }

                var total = drayage + gate
                var withholding = drayage * (1 / 100)
                var check = total - withholding
                    
                drayage_total += drayage
                gate_total += gate

                this.total_list.push(total)
                this.withholding_list.push(withholding)
                this.check_list.push(check)
            }
            this.sum_total = [drayage_total, gate_total, "", sumArray(this.total_list), sumArray(this.withholding_list), sumArray(this.check_list)]
        },

        editWeekDetails() {
            this.input_required = false

            if(this.summary_week_modal.week == '' || this.summary_week_modal.date_start == '' || this.summary_week_modal.date_end == ''){
                this.input_required = true
                return false
            }

            if(this.summary_week_modal.year != this.year || this.summary_week_modal.week != this.week){
                api("/summary/api/check-week-exist/", "POST", { year: this.summary_week_modal.year, week: this.summary_week_modal.week }).then((data) => {
                    if(data) {
                        alert("This week is existing.")
                    }
                    else {
                        this.saveEditWeek()
                    }
                })
            }
            else {
                this.saveEditWeek()
            }
        },
        saveEditWeek() {
            api("/summary/api/edit-summary-week/", "POST", { summary_week: this.summary_week_modal }).then((data) => {
                $('#modalSummaryWeek').modal('hide')
                if(data) {
                    window.location.replace("/summary/" + this.summary_week_modal.year + "/" + this.summary_week_modal.month + "/" + this.summary_week_modal.week)      
                }
            })
        },

        editData(customer_data) {
            if(this.edit_data.indexOf(customer_data) === -1) {
                this.edit_data.push(customer_data)
            }
        },
        saveEditCustomerDetail() {
            if(this.edit_data.length){
                this.saving = true
                api("/summary/api/edit-summary-customer-detail/", "POST", { customer_detail: this.edit_data }).then((data) => {
                    this.getSummaryWeekDetails(this.year, this.month, this.week)
                    this.saving = false
                })
            }
        },

        selectCustomer(customer){
            if (event.ctrlKey) {
                window.open("/summary/" + this.year + "/" + this.month + "/" + this.week + "/" + customer)
            }
            else {
                window.open("/summary/" + this.year + "/" + this.month + "/" + this.week + "/" + customer, "_self")
            }
        },

        changeWeekStatus() {
            api("/summary/api/summary-weeks-status/", "POST", {id: this.week_details.id, status: this.week_details.status}).then((data) => {
                this.getSummaryWeekDetails(this.year, this.month, this.week)
            })
        },
    }
})