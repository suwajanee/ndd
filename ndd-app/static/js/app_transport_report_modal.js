var report_modal = new Vue ({

    el: '#modalExpenseReport',
    data: {
        daily_page: true,

        // Initial
        date: '',
        driver_id: '',

        year: '',
        month: '',
        period: '',
        // End Initial

        // Warning
        modal_warning: false,
        expense_format_status: new Array(13),
        // End Warning
        
        // Order Type
        double_show: ['1.1', '3.1', '4.1', '4.2', '5.1', '5.2'],

        order_type_list: [],
        used_order_type_list: [],
        trip_color: {},
        not_fw_trip: [],
        not_bw_trip: [],
        // End Order Type

        // Driver & Truck Select
        search_driver: '',
        driver_list: [],
        truck_list: [],
        // default
        driver_data: {},
        default_truck: {},
        // selected data
        work_driver_data: {},
        work_truck_data: {},
        // End Driver & Truck Select

        // Work Data
        search_work_id: '',
        work_data: {},
        // End Work Data

        // Report Data
        modal_type: 'normal',
        modal_add_mode: false,

        report_work_id: '',
        report_order: {
            driver: '',
            truck: '',
        },
        report_detail: {},
        report_price: {},
        report_co_expense: {},
        report_cus_expense: {},
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
        getModalExpenseReport(report) {
            this.modal_warning = false     
            this.expense_format_status.fill(true)

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
                this.order_type_list = order_type_list[this.modal_type]
                this.getUsedOrderTypeByWorkId(work.work_id, work_order.order_type)

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
                    time: work.time || '',
                    size_20: work.size.startsWith('20'),
                    size_2_container: work.size.startsWith('2X'),
                    customer: work.principal.name,
                    booking_1: work.booking_no,
                    container_1: work.container_no || work.container_1,
                    container_2: work.seal_no || work.container_2
                }

                this.report_detail = Object.assign({}, work_order.detail)
                this.report_price = Object.assign({}, work_order.price)
                this.report_co_expense = Object.assign({}, report.co_expense)
                this.report_cus_expense = Object.assign({}, report.cus_expense)

                this.report_detail.status_fw = this.report_detail.status_fw || ''
                this.report_detail.status_bw = this.report_detail.status_bw || ''
            }
            else {
                this.modal_add_mode = true
                this.search_work_id = ''

                this.modal_type = ''
                this.report_work_id = ''

                this.work_driver_data = this.driver_data || {}
                this.work_truck_data = this.default_truck || {}

                this.report_order = {
                    clear_date: this.date,
                    driver: this.driver_id || '',
                    truck: this.default_truck.id || '',
                    order_type: null,
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

            this.report_order.double_container = false

            if(work_id != this.report_work_id) {
                if(['EP', 'FC'].includes(work_id_substr)) {
                    api("/agent-transport/api/get-agent-transport-work-by-work-id/", "POST", {work_id: work_id}).then((data) => {
                        if(data) {
                            this.modal_type = 'agent-transport'
                            this.order_type_list = order_type_list[this.modal_type]
                            this.getUsedOrderTypeByWorkId(work_id, this.report_order.order_type)
                            this.report_order.order_type = null

                            this.report_work_id = data.work_id
                            this.report_order.work_date = data.date
                            this.work_data = {
                                size_20: data.size.startsWith('20'),
                                size_2_container: data.size.startsWith('2X'),
                                customer: data.principal.name,
                                booking_1: data.booking_no,
                                container_1: data.container_1,
                                container_2: data.container_2,
                            }

                            this.report_detail.status_fw = ''
                            this.report_detail.status_bw = work_id_substr == 'EP' ? 'e':'f'
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
                            this.order_type_list = order_type_list[this.modal_type]
                            this.getUsedOrderTypeByWorkId(work_id, this.report_order.order_type)
                            this.report_order.order_type = null

                            this.report_work_id = data.work_id
                            this.report_order.work_date = data.date
                            this.work_data = {
                                time: data.time,
                                size_20: data.size.startsWith('20'),
                                size_2_container: data.size.startsWith('2X'),
                                customer: data.principal.name,
                                booking_1: data.booking_no,
                                container_1: data.container_no,
                                container_2: data.seal_no
                            }

                            this.report_detail.status_fw = 'e'
                            this.report_detail.status_bw = 'f'
                        }
                        else {
                            this.report_work_id = ''
                        }
                    })
                }
            }
        },
        getUsedOrderTypeByWorkId(work_id, order_type) {
            api("/report/api/get-used-order-type-by-work-id/", "POST", {work_id: work_id}).then((data) => {
                if(data) {
                    this.used_order_type_list = data

                    if(order_type != null) {
                        var index = this.used_order_type_list.indexOf(order_type)
                        this.used_order_type_list.splice(index, 1)
                    }
                }
            })
        },
        setStatusTrip() {
            if(this.modal_type == 'normal') {
                this.report_order.double_container = false

                this.report_detail.status_fw = 'e'
                this.report_detail.status_bw = 'f'

                if(this.not_fw_trip.includes(this.report_order.order_type)) {
                    this.report_detail.status_fw = ''
                }
                else if(this.not_bw_trip.includes(this.report_order.order_type)) {
                    this.report_detail.status_bw = ''
                }
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
                this.$set(this.expense_format_status, index, true)
            }
            catch {
                this.$set(this.expense_format_status, index, false)
            }
        },

        // ใช้ใน HTML
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

        actionExpenseReport(action) {
            this.modal_warning = false
            
            var expense_status = this.expense_format_status.every(Boolean)

            if(!this.report_order.driver || !this.report_order.truck || !this.modal_type || !this.report_work_id || this.report_order.order_type == null || ! expense_status) {
                this.modal_warning = true
            }
            else {

                if(! this.report_order.double_container) {
                    this.report_detail.container_2 = ''
                    this.report_detail.booking_2 = ''
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

                var url = `/report/api/${action}-expense-report/`

                api(url, "POST", work_data).then((data) => {
                    if(data=='Success') {
                        $('#modalExpenseReport').modal('hide')
                        this.pageReload()
                    }
                }).catch((error) => {
                    alert('Save again')
                    console.error(error)
                })
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
                    daily_report_page.getDailyDriverExpense()
                }
                else {
                    daily_report_page.getDailyExpense()
                }
            }
            else {
                expense_page.filterReport()
            }
        }
    }

})
