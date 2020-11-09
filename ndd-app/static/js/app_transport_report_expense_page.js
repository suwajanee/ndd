var expense_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,
        
        // Initial
        page: '',
        year: '',
        month: '',
        period: '',
        // End Initial

        // Upper Part
        show_filter_btn: true,
        show_col_select: true,

        year_list: [],
        month_list: [],
        full_month_list: [],
        period_num: [],

        col_price: true,
        col_allowance: true,
        col_remark: true,
        // End Upper Part

        // Trip Color
        trip_color: {},
        not_fw_trip: [],
        not_bw_trip: [],
        // End Trip Color

        // Report Data
        from_date: '',
        to_date: '',
        // data list
        report_list: [],
        pk_list: [],
        date_list: [],
        date_report_list: [],
        // total
        total_price_list: [],
        total_expense_list: [],
        // End Report Data
        
        // Filter
        filter_mode: false,
        modal_warning: false,
        // work id input
        work_id: '',
        // driver & truck select
        driver_list: [],
        truck_list: [],
        search_driver: '',
        driver_data: {},
        driver_id: '',
        truck_data: {},
        truck_id: '',
        // select all
        all_customer: true,
        all_remark: true,
        // multiselect
        customer_list: [],
        remark_list: [],
        customer_selected: [],
        remark_selected: [],
        // End Filter
        
    },
    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                var driver_name = driver.employee.full_name
                return driver_name.toLowerCase().includes(search)
            })
        }
    },
    methods: {
        reload(page, year, month, period) {
            this.page = page.toLowerCase()
            this.year = year
            this.month = month
            this.period = period

            this.trip_color = report_modal.trip_color = trip_color
            this.not_fw_trip = report_modal.not_fw_trip = not_fw_trip
            this.not_bw_trip = report_modal.not_bw_trip = not_bw_trip
            
            this.getYear()
            this.month_list = _month
            this.full_month_list = _full_month

            this.getReport()

            if(this.page == 'summary') {
                this.show_col_select = false
            }

            report_modal.daily_page = false
        },

        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },

        changeUrl(period) {
            var url = `/report/${this.page}/${this.year}/${this.month}`
            if(period > 0) {
                url += "/" + period
            }

            window.open(url, "_self")
        },

        getReport() {
            this.loading = true
            var params = {
                page: this.page,
                year: this.year,
                month: this.month,
                period: this.period
            }
            api("/report/api/get-expense-report/", "POST", params).then((data) => {
                this.from_date = data.from_date
                this.to_date = data.to_date
                
                this.report_list = data.report_list
                this.period_num = data.period
                
                this.total_price_list = data.total_price_list

                this.pk_list = data.pk_list

                this.driver_list = report_modal.driver_list = data.driver_list
                this.truck_list = report_modal.truck_list = data.truck_list

                this.customer_list = this.customer_selected = data.customer_list
                this.remark_list = this.remark_selected = data.remark_list

                if(this.page == 'expense') {
                    this.date_list = data.date_list
                    this.total_expense_list = data.total_expense_list
                    this.setDateReport()
                }
                this.loading = false
            })
        },
        filterReport() {
            this.modal_warning = false
            if((this.customer_list.length && ! this.customer_selected.length) || (this.remark_list.length && ! this.remark_selected.length)) {
                this.modal_warning = true
            }
            else {
                this.loading = true

                this.checkFilterMode()
                var data = {
                    page: this.page,
                    pk_list: this.pk_list,
                    work: this.work_id.trim(),
                    driver: this.driver_id,
                    truck: this.truck_id,
                }

                if(this.all_customer) {
                    data.customers = []
                }
                else {
                    data.customers = this.customer_selected
                }

                if(this.all_remark) {
                    data.remarks = []
                }
                else {
                    data.remarks = this.remark_selected
                }
                
                api("/report/api/filter-expense-report/", "POST", data).then((data) => {
                    this.report_list = data.report_list
                    this.total_price_list = data.total_price_list

                    if(this.all_customer) {
                        this.customer_selected = this.customer_list
                    }

                    if(this.all_remark) {
                        this.remark_selected = this.remark_list
                    }

                    if(this.page == 'expense') {
                        this.date_list = data.date_list
                        this.total_expense_list = data.total_expense_list
                        this.setDateReport()
                    }
                    this.loading = false
                })
            }     
        },
        checkFilterMode() {
            if(this.work_id || this.driver_id || this.truck_id || ! this.all_customer || ! this.all_remark) {
                this.filter_mode = true
            }
            else {
                this.filter_mode = false
            }
        },
        setDateReport() {
            this.date_report_list = []
            this.date_list.forEach((date) => {
                var report_result = this.report_list.filter(report => report.work_order.clear_date === date)

                var co_total = sumObjectArray(report_result, 'co_total')
                var cus_total = sumObjectArray(report_result, 'cus_total')

                var report = {
                    clear_date: date,
                    report_list: report_result,
                    total: co_total + cus_total
                }
                this.date_report_list.push(report)

            })
        },

        clearFilter() {
            this.work_id = ''

            this.driver_id = ''
            this.driver_data = {}
            this.truck_id = ''
            this.truck_data = {}

            this.all_customer = true
            this.customer_selected = this.customer_list
            this.all_remark = true
            this.remark_selected = this.remark_list

            this.filterReport()
        },

        selectDriver(driver) {
            if(driver) {
                this.driver_id = driver.id
                this.driver_data = driver.employee
            }
            else {
                this.driver_id = ''
                this.driver_data = {}
            }
            
        },
        selectTruck(truck) {
            if(truck) {
                this.truck_id = truck.id
                this.truck_data = truck
            }
            else {
                this.truck_id = ''
                this.truck_data = {}
            }
        },

        multiSelectAll(input) {
            if(this['all_' + input]) {
                this[input + '_selected'] = this[input + '_list']
            }
            else {
                this[input + '_selected'] = []
            }
        },
        multiSelectCheck(input) {
            if(this[input + '_selected'].length == this[input + '_list'].length) {
                this['all_' + input] = true
            }
            else {
                this['all_' + input] = false
            }
        },
    }
})