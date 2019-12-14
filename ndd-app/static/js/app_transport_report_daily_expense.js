var daily_expense_page = new Vue ({

    el: '#daily-expense-page',
    data: {
        page: '',

        co: '',
        date: '',

        driver_list: [],
        report_list: [],
        
        transport_list: []
    },

    methods: {
        reload(date, co) {
            this.date = date
            this.co = co

            this.getActiveDriver()
            this.getDailyExpense(date, co)
        },

        filterDate(){
            window.open("/transport-report/daily-expense/" + this.date + "/" + this.co, "_self")
        },

        getDailyExpense(date, co) {
            if(date && co) {
                api("/transport-report/api/get-daily-expense/", "POST", {date: date, co: co}).then((data) => {
                    this.date = data.date
                    this.report_list = data.work_expense
                    this.matchDriverReport()
                    
                })
            }
            else {
                api("/transport-report/api/get-daily-expense/").then((data) => {
                    this.date = data.date
                    this.report_list = data.work_expense
                    this.matchDriverReport()
                })
            }
        },

        matchDriverReport() {
            var not_active_index = []
            this.driver_list.forEach((driver, index) => {
                var report_result = this.report_list.filter(report => report.work_order.driver.id === driver.id)
                driver['report_list'] = report_result

                if(driver.employee.status === 't' && driver.report_list.length == 0) {
                    not_active_index.push(index)
                }
            })

            not_active_index.forEach((item, index) => {
                item = item - index
                this.driver_list.splice(item, 1)
            })

        },



        getActiveDriver() {
            api("/employee/api/get-all-driver/", "POST", {co: this.co}).then((data) => {
                // console.log(data)
                this.driver_list = data
                console.log(2222)
                console.log(this.driver_list)
            })
        },
        
    }
})
