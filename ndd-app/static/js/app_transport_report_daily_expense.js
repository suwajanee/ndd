var daily_expense_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,
        page: '',

        co: '',
        date: '',
        driver_id: '',

        driver_data: {},
        search_driver: '',
        driver_list: [],
        truck_list: [],

        driver_report_list: [],
        expense_list: [],
        
        transport_list: [],

        col_price: true,
        col_allowance: true,
        col_remark: false,
        // show_allowance: true,
        // show_col: ['price', 'allowance'],

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
        reload(date, co, driver) {
            this.date = report_modal.date = date
            this.co = report_modal.co = co
            
            this.getActiveDriver()
            this.getActiveTruck()
            if(driver) {
                this.driver_id = report_modal.driver_id = driver
                this.getDailyDriverExpense()
            }
            else {
                this.getAllDriver()
                this.getDailyExpense()
            }
        },
    

        changeUrl(driver) {
            if(driver){
                window.open("/transport-report/daily-expense/" + this.date + "/" + driver, "_self")
            }
            else {
                window.open("/transport-report/daily-expense/" + this.date + "/" + this.co, "_self")
            }
        },

        getDailyExpense() {
            this.loading = true
            if(this.date && this.co) {
                api("/transport-report/api/get-daily-expense/", "POST", {date: this.date, co: this.co}).then((data) => {
                    if(! data) {
                        window.location.replace("/dashboard")
                        return false
                    }
                    this.date = data.date
                    this.expense_list = data.work_expense
                    this.matchDriverReport()
                    this.loading = false 
                })
            }
            else {
                api("/transport-report/api/get-daily-expense/").then((data) => {
                    this.date = data.date
                    this.expense_list = data.work_expense
                    this.matchDriverReport()
                    this.loading = false
                })
            }
        },
        getDailyDriverExpense() {
            this.loading = true
            api("/transport-report/api/get-daily-driver-expense/", "POST", {date: this.date, driver: this.driver_id}).then((data) => {
                if(! data) {
                    window.location.replace("/dashboard")
                    return false
                }
                this.driver_data = report_modal.driver_data = data.driver
                report_modal.default_truck = data.truck
                this.expense_list = data.report
                
                this.driver_data['total'] = []
                this.driver_data['total'][0] = this.calcTotalExpense(this.expense_list[0])
                this.driver_data['total'][1] = this.calcTotalExpense(this.expense_list[1])

                this.loading = false
            })
        },


        matchDriverReport() {
            var not_active_index = []
            this.driver_report_list.forEach((driver, index) => {
                var report_result = this.expense_list.filter(report => report.work_order.driver.id === driver.id)
                driver['report_list'] = report_result

                driver['total'] = this.calcTotalExpense(report_result)

                if((driver.employee.status === 't' || driver.employee.co != this.co) && driver.report_list.length == 0) {
                    not_active_index.push(index)
                }
            })

            not_active_index.forEach((item, index) => {
                item = item - index
                this.driver_report_list.splice(item, 1)
            })

        },
        calcTotalExpense(array) {
            var co_total = sumObjectArray(array, 'total_expense', 'company')
            var cus_total = sumObjectArray(array, 'total_expense', 'customer')
            return co_total + cus_total
        },

        getActiveDriver() {
            api("/employee/api/get-active-driver/", "POST", {co: this.co}).then((data) => {
                this.driver_list = report_modal.driver_list = data
            })
        },
        getAllDriver() {
            api("/employee/api/get-all-driver/", "POST", {co: this.co}).then((data) => {
                this.driver_report_list = data
            })
        },

        getActiveTruck() {
            api("/truck-chassis/api/get-active-truck/", "POST", {co: this.co}).then((data) => {
                this.truck_list = report_modal.truck_list = data
            })
        },

        
        
    }
})
