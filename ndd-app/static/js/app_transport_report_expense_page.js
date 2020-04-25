var expense_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,
        year: '',
        month: '',
        co: '',
        period: '',

        year_list: [],
        month_list: [],
        full_month_list: [],

        col_price: true,
        col_allowance: true,
        col_remark: true,

        report_list: [],
        period_num: [],
        total_price_list: [],
        total_expense_list: [],

        driver_list: [],
        truck_list: [],

        // filter
        filter_mode: false,
        modal_warning: false,

        search_driver: '',
        driver_data: {
            // co: ''
        },
        driver_id: '',
        truck_data: {},
        truck_id: '',

        pk_list: [],
        // work_list: [],
        customer_list: [],
        remark_list: [],

        all_customer: true,
        all_remark: true,

        work_id: '',
        customer_selected: [],
        remark_selected: [],
        
    },
    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                var driver_name = driver.employee.detail.full_name
                return driver_name.toLowerCase().includes(search)
            })
        }
    },
    methods: {
        reload(year, month, co, period) {
            this.year = year
            this.month = month
            this.co = report_modal.co = co
            this.period = period
            
            this.getYear()
            this.month_list = _month
            this.full_month_list = _full_month

            this.getActiveDriver()
            this.getActiveTruck()
            this.getExpenseReport()

            report_modal.daily_page = false
        },

        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },

        changeUrl(period) {
            if(period > 0) {
                window.open("/report/expense/" + this.year + "/" + this.month + "/" + this.co + "/" + period, "_self")
            }
            else {
                window.open("/report/expense/" + this.year + "/" + this.month + "/" + this.co, "_self")
            }
        },

        getExpenseReport() {
            this.loading = true
            var filter = {
                year: this.year,
                month: this.month,
                co: this.co,
                period: this.period
            }
            api("/report/api/get-expense-report/", "POST", filter).then((data) => {
                this.report_list = data.expense
                this.period_num = data.period

                this.total_price_list = data.total[0]
                this.total_expense_list = data.total[1]

                this.pk_list = data.pk_list

                this.customer_list = this.customer_selected = data.customer_list
                this.remark_list = this.remark_selected = data.remark_list

                this.loading = false
            })
        },
        checkFilterMode() {
            if(this.work_id || this.driver_id || this.truck_id || ! this.all_customer || ! this.all_remark) {
                this.filter_mode = true
            }
            else {
                this.filter_mode = false
            }
        },

        filterExpenseReport() {
            this.modal_warning = false
            if((this.customer_list.length && ! this.customer_selected.length) || (this.remark_list.length && ! this.remark_selected.length)) {
                this.modal_warning = true
            }
            else {
                this.loading = true

                this.checkFilterMode()
                var data = {
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
                    this.report_list = data.expense
                    this.total_price_list = data.total[0]
                    this.total_expense_list = data.total[1]

                    if(this.all_customer) {
                        this.customer_list = this.customer_selected = data.customer_list
                    }
                    else {
                        this.customer_list = data.customer_list
                        this.customer_selected = this.customer_list.filter(customer => this.customer_selected.includes(customer))
                    }

                    if(this.all_remark) {
                        this.remark_list = this.remark_selected = data.remark_list
                    }
                    else {
                        this.remark_list = data.remark_list
                        this.remark_selected = this.remark_list.filter(remark => this.remark_selected.includes(remark))
                    }
                    this.loading = false
                })
            }     
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

            this.filterExpenseReport()

        },

        getActiveDriver() {
            api("/employee/api/get-active-driver/", "POST", {co: this.co}).then((data) => {
                this.driver_list = report_modal.driver_list = data
            })
        },
        getActiveTruck() {
            api("/truck-chassis/api/get-active-truck/", "POST", {co: this.co}).then((data) => {
                this.truck_list = report_modal.truck_list = data
            })
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