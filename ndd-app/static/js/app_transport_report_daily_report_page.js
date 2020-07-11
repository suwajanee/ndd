var daily_report_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,

        date: '',
        driver_id: '',

        driver_data: {},
        search_driver: '',
        driver_list: [],
        truck_list: [],

        driver_report_list: [],
        expense_list: [],
        total: 0,
        
        col_price: true,
        col_allowance: true,
        col_remark: false,
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
        reload(date, driver) {
            this.date = report_modal.date = date

            report_modal.trip_color = trip_color
            report_modal.not_fw_trip = not_fw_trip
            report_modal.not_bw_trip = not_bw_trip
            
            this.getActiveDriver()
            this.getActiveTruck()
            if(driver) {
                this.driver_id = report_modal.driver_id = driver
                this.getDailyDriverExpense()
            }
            else {
                this.getDailyExpense()
            }
        },
    

        changeUrl(driver) {
            var url = "/report/daily-report/" + this.date + "/"
            if(driver){
                url += driver
            }
            // else {
            //     url += this.co
            // }
            window.open(url, "_self")
        },

        getDailyExpense() {
            this.loading = true
            api("/report/api/get-daily-report/", "POST", {date: this.date}).then((data) => {
                if(! data) {
                    window.location.replace("/dashboard")
                    return false
                }
                this.date = data.date
                this.expense_list = data.expense_list
                this.driver_report_list = data.driver_list
                this.total = data.total

                this.matchDriverReport()
            })
        },
        matchDriverReport() {
            this.driver_report_list.forEach((driver) => {
                var report_result = this.expense_list.filter(report => report.work_order.driver.id === driver.id)
                driver['report_list'] = report_result

                driver['total'] = this.calcTotalExpense(report_result)
            })
            this.loading = false 
        },
        
        getDailyDriverExpense() {
            this.loading = true
            api("/report/api/get-daily-driver-report/", "POST", {date: this.date, driver: this.driver_id}).then((data) => {
                if(! data) {
                    window.location.replace("/dashboard")
                    return false
                }
                this.driver_data = report_modal.driver_data = data.driver
                report_modal.default_truck = data.truck
                this.expense_list = data.expense_list
                this.total = this.calcTotalExpense(this.expense_list)

                this.loading = false
            })
        },
        
        calcTotalExpense(array) {
            var co_total = sumObjectArray(array, 'co_total')
            var cus_total = sumObjectArray(array, 'cus_total')
            return co_total + cus_total
        },

        getActiveDriver() {
            api("/employee/api/get-active-driver/").then((data) => {
                this.driver_list = report_modal.driver_list = data
            })
        },

        getActiveTruck() {
            api("/truck-chassis/api/get-active-truck/").then((data) => {
                this.truck_list = report_modal.truck_list = data
            })
        },

        
        
    }
})
