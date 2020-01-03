var daily_expense_page = new Vue ({

    el: '#daily-expense-page',
    data: {
        page: '',

        co: '',
        date: '',
        driver_id: '',

        driver_data: {},
        defualt_truck: '',
        search_driver: '',
        driver_list: [],

        driver_report_list: [],
        expense_list: [],
        
        transport_list: []
    },

    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                return driver.employee.first_name.toLowerCase().includes(search) || driver.employee.last_name.trim().toLowerCase().includes(search)
            })
        }
    },

    methods: {
        date_reload(date, co) {
            this.date = date
            this.co = co

            this.getActiveDriver()
            this.getAllDriver()
            this.getDailyExpense()
        },
        driver_reload(date, driver) {
            this.date = date
            this.driver_id = driver

            this.getActiveDriver()
            this.getDailyDriverExpense()
        },

        show_note() {
            var tbody = document.getElementById("tbody")
            tbody.addEventListener('mousedown', function(e) {
                e = e || window.event
                var target = e.target 
                var alert = target.children[0]
                if(alert && target.tagName == "TD") {
                    alert.style.display = "block"                   
                }
            }, false)  
        },

        hide_note() {
            var tbody = document.getElementById("tbody")
            tbody.addEventListener('mouseup', function(e) {
                e = e || window.event
                var target = e.target
                var alert = target.children[0]
                if(alert && target.tagName == "TD") {
                    alert.style.display = "none"
                }
            }, false)
        },

        urlFormat(driver) {
            if(driver){
                window.open("/transport-report/daily-expense/" + this.date + "/" + driver, "_self")
            }
            else {
                window.open("/transport-report/daily-expense/" + this.date + "/" + this.co, "_self")
            }
        },

        getDailyExpense() {
            if(this.date && this.co) {
                api("/transport-report/api/get-daily-expense/", "POST", {date: this.date, co: this.co}).then((data) => {
                    this.date = data.date
                    this.expense_list = data.work_expense
                    this.matchDriverReport()
                    
                })
            }
            else {
                api("/transport-report/api/get-daily-expense/").then((data) => {
                    this.date = data.date
                    this.expense_list = data.work_expense
                    this.matchDriverReport()
                })
            }
        },
        getDailyDriverExpense() {
            api("/transport-report/api/get-daily-driver-expense/", "POST", {date: this.date, driver: this.driver_id}).then((data) => {
                this.driver_data = data.driver
                this.default_truck = data.truck
                this.expense_list = data.report

                this.co = this.driver_data.co

                this.driver_data['total'] = this.calcTotalExpense(this.expense_list)
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
                this.driver_list = data
            })
        },
        getAllDriver() {
            api("/employee/api/get-all-driver/", "POST", {co: this.co}).then((data) => {
                this.driver_report_list = data
            })
        },
        
    }
})
