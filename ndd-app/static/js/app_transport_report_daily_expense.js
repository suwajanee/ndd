var daily_expense_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,
        page: '',

        co: '',
        date: '',
        driver_id: '',

        driver_data: {},
        default_truck: '',
        search_driver: '',
        driver_list: [],
        truck_list: [],

        driver_report_list: [],
        expense_list: [],
        
        transport_list: [],

        modal_warning: false,
        modal_add_mode: false,
        search_work_id: '',
        double_show: ['1.1', '3.1', '4.1', '4.2', '5.1', '5.2'],
        work_data: {},
        work_driver_data: {
            co: '',
        },
        work_truck_data: {
            owner: '',
        },

        modal_type: 'normal',
        report_work_id: '',
        report_order: {
            driver: '',
            truck: '',
        },
        report_detail: {},
        report_price: {},
        report_co_expense: {},
        report_cus_expense: {},

        expense_format_status: {},

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
        reload(date, co, driver) {
            this.date = date
            this.co = co
            
            this.getActiveDriver()
            this.getActiveTruck()
            if(driver) {
                this.driver_id = driver
                this.getDailyDriverExpense()
            }
            else {
                this.getAllDriver()
                this.getDailyExpense()
            }
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
            this.loading = true
            if(this.date && this.co) {
                api("/transport-report/api/get-daily-expense/", "POST", {date: this.date, co: this.co}).then((data) => {
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
                this.driver_data = data.driver
                this.default_truck = data.truck
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
                this.driver_list = data
            })
        },
        getAllDriver() {
            api("/employee/api/get-all-driver/", "POST", {co: this.co}).then((data) => {
                this.driver_report_list = data
            })
        },

        getActiveTruck() {
            api("/truck-chassis/api/get-active-truck/", "POST", {co: this.co}).then((data) => {
                this.truck_list = data
            })
        },


        modalReport(report) {

            this.expense_format_status = {
                0: true,
                1: true,
                2: true,
                3: true,
                4: true,
                5: true,
                6: true,

                7: true,
                8: true,
                9: true,

                10: true,
                11: true,
                12: true,
            }
  
            if(report) {
                this.modal_add_mode = false
                this.search_work_id = ''
                
                var work_order = report.work_order
                var work = work_order.work
                
                this.modal_type = work.principal.work_type
                this.report_work_id = work.work_id
                this.search_work_id = work.work_id

                this.work_driver_data = work_order.driver.employee
                this.work_truck_data = work_order.truck

                this.report_order = {
                    pk: work_order.id,
                    driver: work_order.driver.employee.id,
                    truck: work_order.truck.id,
                    clear_date: work_order.clear_date,
                    work_date: work_order.work_date,
                    order_type: work_order.order_type,
                    double_container: work_order.double_container,

                    expense_pk: report.id,
                }
                this.work_data = {
                    size: work.size.indexOf('20'),
                    customer: work.principal.name,
                }
                this.report_detail = Object.assign({}, work_order.detail)
                this.report_price = Object.assign({}, work_order.price)
                this.report_co_expense = Object.assign({}, report.co_expense)
                this.report_cus_expense = Object.assign({}, report.cus_expense)
            }
            else {
                this.modal_add_mode = true
                this.search_work_id = ''

                this.modal_type = ''
                this.report_work_id = ''

                this.work_driver_data = this.driver_data
                this.work_truck_data = this.default_truck

                this.report_order = {
                    clear_date: this.date,
                    driver: this.driver_id,
                    truck: this.default_truck.id || '',
                    order_type: '',
                    double_container: false,
                }
                this.report_detail = {}
                this.report_price = {}
                this.report_co_expense = {}
                this.report_cus_expense = {}
                this.work_data = {}

            }
        },

        getWorkByworkId(work_id) {
            work_id = work_id.trim().toUpperCase()
            var work_id_substr = work_id.substr(0, 2)

            this.report_order.order_type = ''
            this.report_order.double_container = false
            if(['EP', 'FC'].includes(work_id_substr)) {
                api("/agent-transport/api/get-agent-transport-work-by-work-id/", "POST", {work_id: work_id}).then((data) => {
                    if(data) {
                        this.modal_type = 'agent-transport'
                        this.report_work_id = data.work_id
                        this.report_order.work_date = data.date
                        this.work_data = {
                            size: data.size.indexOf('20'),
                            customer: data.principal.name,
                        }
                    }
                    else {
                        this.report_work_id = ''
                    }
                })
            }
            else {
                api("/booking/api/get-normal-work-by-work-id/", "POST", {work_id: work_id}).then((data) => {
                    if(data) {
                        this.modal_type = 'normal'
                        this.report_work_id = data.work_id
                        this.report_order.work_date = data.date
                        this.work_data = {
                            size: data.size.indexOf('20'),
                            customer: data.principal.name,
                        }
                    }
                    else {
                        this.report_work_id = ''
                    }
                })

            }
        },
        selectDriver(driver) {
            this.report_order.driver = driver.employee.id
            this.work_driver_data = driver.employee

            if(driver.truck) {
                this.report_order.truck = driver.truck.id
                this.work_truck_data = driver.truck
            }
            else {
                this.report_order.truck = ''
                this.work_truck_data = {}
            }
        },
        selectTruck(truck) {
            this.report_order.truck = truck.id
            this.work_truck_data = truck
        },

        // เช็ค String Format (Expense)
        checkExpenseFormat(str, index) {
            try {
                eval(str)
                this.expense_format_status[index] = true
            }
            catch {
                this.expense_format_status[index] = false
            }
        },

        sumString(str) {
            try {
                return eval(str)
            }
            catch {
                return 0
            }

        },

        totalExpense(obj) {
            var array = Object.values(obj)
            return sumStringArray(array)
        },


        addOrEditExpenseReport() {
            this.modal_warning = false

            var status_array = Object.values(this.expense_format_status)
            var expense_status = status_array.every(Boolean)

            if(!this.report_order.driver || !this.report_order.truck || !this.modal_type || !this.report_work_id || !expense_status) {
                this.modal_warning = true
                return false
            }
            else {
                remove_empty_key(this.report_detail)
                remove_empty_key(this.report_co_expense)
                remove_empty_key(this.report_cus_expense)
                remove_empty_key(this.report_price)

                var total = {
                    company: this.totalExpense(this.report_co_expense),
                    customer: this.totalExpense(this.report_cus_expense)
                }

                var work_data = {
                    work_type: this.modal_type,
                    work_id: this.report_work_id,
                    work_order: this.report_order,
                    detail: this.report_detail,
                    price: this.report_price,
                    co_expense: this.report_co_expense,
                    cus_expense: this. report_cus_expense,
                    total_expense: total
                }
                if(this.modal_add_mode) {
                    api("/transport-report/api/add-expense-report/", "POST", work_data).then((data) => {
                        if(data=='Success') {
                            this.urlFormat(this.driver_id)
                        }
                    })
                }
                else {
                    api("/transport-report/api/edit-expense-report/", "POST", work_data).then((data) => {
                        if(data=='Success') {
                            if(this.driver_id) {
                                this.urlFormat(this.driver_id)
                            }
                            else {
                                this.urlFormat()
                            }
                        }
                    })
                }
                
            }

        }
        
    }
})
