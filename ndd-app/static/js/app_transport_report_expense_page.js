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
        period_list: [],

        driver_list: [],
        truck_list: [],

        // filter
        search_driver: '',
        driver_data: {
            // co: ''
        },
        driver_id: '',
        truck_data: {},
        truck_id: '',

        pk_list: [],
        work_list: [],
        customer_list: [],
        remark_list: [],
        
    },
    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                var driver_name = driver.employee.first_name + ' ' + driver.employee.last_name
                return driver_name.toLowerCase().includes(search)
            })
        }
    },


    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                var driver_name = driver.employee.first_name + ' ' + driver.employee.last_name
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
                this.period_list = data.period

                this.pk_list = data.pk_list
                this.work_list = data.work_list
                this.customer_list = data.customer_list
                this.remark_list = data.remark_list

                this.loading = false
            })
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
        }




        
    }
})