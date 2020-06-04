var report_modal = new Vue ({

    el: '#modalExpenseReport',
    data: {
        daily_page: true,

        co: '',
        date: '',
        driver_id: '',

        year: '',
        month: '',
        period: '',

        search_driver: '',
        driver_list: [],
        truck_list: [],
        driver_data: {},
        default_truck: {},

        modal_warning: false,
        modal_add_mode: false,
        search_work_id: '',
        double_show: ['1.1', '3.1', '4.1', '4.2', '5.1', '5.2'],

        work_data: {},
        work_driver_data: {
            co: '',
            detail: {}
        },
        work_truck_data: {
            owner: ''
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
                var driver_name = driver.employee.full_name
                return driver_name.toLowerCase().includes(search)
            })
        }
    },

    methods: {
        getModalExpenseReport(report) {
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
                if(work_order.work_normal) {
                    var work = work_order.work_normal
                }
                else {
                    var work = work_order.work_agent_transport
                }
                
                this.modal_type = work.principal.work_type
                this.report_work_id = this.search_work_id = work.work_id
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

                    expense_pk: report.id
                }

                this.work_data = {
                    size_20: work.size.startsWith('20'),
                    size_2_container: work.size.startsWith('2X'),
                    customer: work.principal.name,
                    container_1: work.container_no || work.container_1,
                    container_2: work.seal_no || work.container_2
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

        getWorkByWorkId(work_id) {
            work_id = work_id.trim().toUpperCase()
            var work_id_substr = work_id.substr(0, 2)

            this.report_order.order_type = ''
            this.report_order.double_container = false
            if(['EP', 'FC'].includes(work_id_substr)) {
                api("/agent-transport/api/get-agent-transport-work-by-work-id/", "POST", {work_id: work_id}).then((data) => {
                    if(data) {
                        this.modal_type = 'agent-transprot'
                        this.report_work_id = data.work_id
                        this.report_order.work_date = data.date
                        this.work_data = {
                            size_20: data.size.startsWith('20'),
                            size_2_container: data.size.startsWith('2X'),
                            customer: data.principal.name,
                            container_1: data.container_1,
                            container_2: data.container_2,
                        }
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
                            size_20: data.size.startsWith('20'),
                            size_2_container: data.size.startsWith('2X'),
                            customer: data.principal.name,
                            container_1: data.container_no,
                            container_2: data.seal_no
                        }
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
            }
            else {

                if(! this.report_order.double_container) {
                    this.report_detail.container_2 = ''
                }
                remove_empty_key(this.report_detail)
                remove_empty_key(this.report_price)
                remove_empty_key(this.report_co_expense)
                remove_empty_key(this.report_cus_expense)

                
                co_total = this.totalExpense(this.report_co_expense),
                cus_total = this.totalExpense(this.report_cus_expense)
                
                var work_data = {
                    work_type: this.modal_type,
                    work_id: this.report_work_id,
                    work_order: this.report_order,
                    detail: this.report_detail,
                    price: this.report_price,
                    co_expense: this.report_co_expense,
                    cus_expense: this.report_cus_expense,
                    co_total: co_total,
                    cus_total: cus_total
                }

                if(this.modal_add_mode) {
                    api("/report/api/add-expense-report/", "POST", work_data).then((data) => {
                        if(data=='Success') {
                            $('#modalExpenseReport').modal('hide');
                            daily_expense_page.getDailyDriverExpense()
                        }
                    })
                }
                else {
                    api("/report/api/edit-expense-report/", "POST", work_data).then((data) => {
                        if(data=='Success') {
                            $('#modalExpenseReport').modal('hide');
                            this.pageReload()
                        }
                    }).catch((error) => {
                        alert('Save again')
                        console.error(error)
                    })
                }

            }
        },

        deleteExpenseReport(id) {
            if(confirm('Are you sure?')) {
                api("/report/api/delete-expense-report/", "POST", {id: id}).then((data) => {
                    if(data=='Success') {
                        $('#modalExpenseReport').modal('hide');
                        this.pageReload()
                    }
                })
            }
        },

        pageReload() {
            if(this.daily_page) {
                if(this.driver_id) {
                    daily_expense_page.getDailyDriverExpense()
                }
                else {
                    daily_expense_page.getDailyExpense()
                }
            }
            else {
                expense_page.filterReport()
            }
        }
    }

})

