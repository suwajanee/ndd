var daily_report_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,

        // Initial
        date: '',
        driver_id: '',
        // End Initial

        // Upper Part
        col_price: true,
        col_allowance: true,
        col_remark: true,
        col_edit: true,
        // End Upper Part

        // Driver Select
        driver_data: {}, // selected data
        search_driver: '',
        driver_list: [],
        // End Driver Select

        // Report Data
        expense_list: [],
        total: 0,
        // End Report Data
        
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
            
            if(driver) {
                this.driver_id = report_modal.driver_id = report_modal.default_driver_id = driver
                this.getDailyDriverExpense()
                this.getDefaultDriverTruck()
            }
            else {
                this.getDailyExpense()
            }
        },

        changeUrl(driver) {
            var url = `/report/daily-report/${this.date}/`
            if(driver){
                url += driver
            }
            window.open(url, "_self")
        },

        getDailyExpense() {
            this.loading = true
            api("/report/api/get-daily-report/", "POST", {date: this.date}).then((data) => {
                if(! data) {
                    window.location.replace("/dashboard")
                    return false
                }
                this.expense_list = data.expense_list
                this.driver_list = report_modal.driver_list = data.driver_list
                report_modal.truck_list = data.truck_list
                this.total = data.total

                this.matchDriverReport()
            })
        },
        matchDriverReport() {
            this.driver_list.forEach((driver) => {
                var report_result = this.expense_list.filter(report => report.work_order.driver.id === driver.id)
                driver['report_list'] = report_result

                driver['total'] = this.calcTotalExpense(report_result)
            })
            this.loading = false 
        },
        
        getDefaultDriverTruck() {
            api("/report/api/get-default-driver-truck/", "POST", {driver_id: this.driver_id}).then((data) => {
                if(! data) {
                    this.changeUrl()
                }
                this.driver_data = report_modal.driver_data = report_modal.default_driver_data = data.driver
                report_modal.default_truck = data.truck
            })
        },
        getDailyDriverExpense() {
            this.loading = true
            api("/report/api/get-daily-report/", "POST", {date: this.date, driver: this.driver_id}).then((data) => {
                if(! data) {
                    window.location.replace("/dashboard")
                    return false
                }
                this.driver_list = report_modal.driver_list = data.driver_list
                report_modal.truck_list = data.truck_list
                
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
    }
})
