var daily_expense_page = new Vue ({

    el: '#expense-page',
    data: {
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

        // empty_order: {
        //     driver: '',
        //     truck: '',
        //     work_id: '',
        //     order_type: '',
        //     double_container: false,
        //     work_date: '',
        // },

        modal_add_mode: false,
        search_work_id: '',
        double_show: ['1.1', '3.1', '4.1', '4.2', '5.1', '5.2'],

        modal_type: 'normal',
        report_work_id: '',
        report_order: {
            driver: '',
            truck: '',
        },
        work_data: {},
        report_detail: {},
        report_co_expense: {},
        report_cus_expense: {},

        // empty_work_data: {},
        // empty_detail: {
        //     customer_name: '',
        //     remark: '',
        //     co_toll_note: '',
        //     co_gate_note: '',
        //     co_tire_note: '',
        //     co_fine_note: '',
        //     co_thc_note: '',
        //     co_service_note: '',
        //     co_other_note: '',
        //     cus_return_note: '',
        //     cus_gate_note: '',
        //     cus_other_note: '',
        // },
        // empty_co_expense: {
        //     co_toll: '',
        //     co_gate: '',
        //     co_tire: '',
        //     co_fine: '',
        //     co_thc: '',
        //     co_service: '',
        //     co_other: ''
        // },
        // empty_cus_expense: {
        //     cus_return: '',
        //     cus_gate: '',
        //     cus_other: ''
        // },

        

        

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

        getActiveTruck() {
            api("/truck-chassis/api/get-active-truck/", "POST", {co: this.co}).then((data) => {
                this.truck_list = data
            })
        },


        modalReport(report) {
            if(report) {
                this.modal_add_mode = false
                this.search_work_id = ''
                
                var work_order = report.work_order
                var work = work_order.work
                
                this.modal_type = work.principal.work_type
                this.report_work_id = work.work_id
                this.report_order = {
                    driver: work_order.driver.employee,
                    truck: work_order.truck,
                    clear_date: work_order.clear_date,
                    work_date: work_order.work_date,
                    // work_id: work.work_id,
                    order_type: work_order.order_type,
                    double_container: work_order.double_container
                }
                this.work_data = {
                    size: work.size.indexOf('20'),
                    customer: work.principal.name,
                }
                this.report_detail = Object.assign({}, work_order.detail)
                this.report_co_expense = Object.assign({}, report.co_expense)
                this.report_cus_expense = Object.assign({}, report.cus_expense)
            }
            else {
                this.modal_add_mode = true
                this.search_work_id = ''
                // this.report_order = Object.assign({}, this.empty_order)
                // this.report_detail = Object.assign({}, this.empty_detail)
                // this.report_co_expense = Object.assign({}, this.empty_co_expense)
                // this.report_cus_expense = Object.assign({}, this.empty_cus_expense)

                // this.work_data = Object.assign({}, this.empty_work_data)
                this.modal_type = ''
                this.report_work_id = ''

                this.report_order = {
                    clear_date: this.date,
                    driver: this.driver_data,
                    truck: this.default_truck || {},
                    order_type: '',
                    double_container: false,
                }
                this.report_detail = {}
                this.report_co_expense = {}
                this.report_cus_expense = {}
                this.work_data = {}

            }
        },

        getWorkByworkId(work_id) {
            var work_id_substr = work_id.substr(0, 2).toLowerCase()

            this.report_order.order_type = ''
            this.report_order.double_container = false
            if(['ep', 'fc'].includes(work_id_substr)) {
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
        }
        
    }
})
