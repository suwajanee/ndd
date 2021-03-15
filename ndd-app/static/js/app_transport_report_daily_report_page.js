var daily_report_page = new Vue ({

    el: '#expense-page',
    data: {
        loading: false,
        edit_table: false,

        // Initial
        date: '',
        driver_id: '',
        key_price: ['work', 'allowance', 'overnight'],
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

        // Report Data & Edit table
        init_expense_list: [],
        expense_list: [],
        filtered_expense_list: [],

        edit_list: [],
        price_status: [true, true, true],

        total_price_list: [],
        total_expense_list: [],
        // End Report Data

        // Filter
        filter_mode: false,
        customer_list: [],
        customer_selected: [],
        all_customer: true,

        price_work_check: [true, false],
        price_allowance_check: [true, false],
        // End Filter
    },

    computed: {
        filterDriver() {
            if(this.search_driver === '') return this.driver_list
            var search = this.search_driver.trim().toLowerCase()
            return this.driver_list.filter(driver => {
                var driver_name = driver.employee.full_name
                return driver_name.toLowerCase().includes(search)
            })
        },
    },

    methods: {
        reload(date, driver) {
            this.date = report_modal.date = date

            report_modal.trip_color = trip_color
            report_modal.not_fw_trip = not_fw_trip
            report_modal.not_bw_trip = not_bw_trip

            var edit_hash = window.location.hash.slice(1)
            if(edit_hash == 'edit') {
                this.edit_table = true
            }

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

                this.init_expense_list = data.expense_list
                this.init_expense_list.forEach(item => {
                    item.work_order.price_status = [true, true, true]
                })
                this.filtered_expense_list = this.expense_list = cloneObject(this.init_expense_list)
                this.customer_list = this.customer_selected = data.customer_list
                this.driver_list = report_modal.driver_list = data.driver_list
                report_modal.truck_list = data.truck_list

                this.calcTotalPriceList()
                this.total_expense_list = data.total_expense_list

                this.matchDriverReport()
            })
        },
        // Group by driver
        matchDriverReport() {
            this.driver_list.forEach((driver) => {
                var report_result = this.init_expense_list.filter(report => report.work_order.driver.id === driver.id)
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

                this.init_expense_list = data.expense_list
                this.init_expense_list.forEach(item => {
                    item.work_order.price_status = [true, true, true]
                })
                this.filtered_expense_list = this.expense_list = cloneObject(this.init_expense_list)
                this.customer_list = this.customer_selected = data.customer_list

                this.calcTotalPriceList()
                this.total_expense_list = data.total_expense_list

                this.loading = false
            })
        },
        // Sum price [work, allowance, overnight]
        calcTotalPriceList() {
            var work_order_list = this.expense_list.map(item => item.work_order.price)
            var total_list = []
            this.key_price.forEach(key => {
                var total = sumObjectArray(work_order_list, key)
                total_list.push(total)
            })
            this.total_price_list = total_list
        },
        // Sum company & customer total
        calcTotalExpense(array) {
            var co_total = sumObjectArray(array, 'co_total')
            var cus_total = sumObjectArray(array, 'cus_total')
            return co_total + cus_total
        },

        // Edit table & Filter
        toggleEditButton(status) {
            if(status) {
                if(this.edit_list.length > 0) {
                    if(confirm("SAVE ?")) {
                        this.saveEditTable()
                        return false
                    }
                    else {
                        this.filtered_expense_list = this.expense_list = cloneObject(this.init_expense_list)
                        if(! this.driver_id) {
                            this.matchDriverReport()
                        }
                    }
                }
                window.history.replaceState("", "", window.location.href.replace("#edit", ""))
                this.edit_table = false
            }
            else {
                window.location.hash = 'edit'
                this.edit_table = true
            }

            this.clearFilter()
            this.edit_list = []
        },
        pushEditList(obj, index=false) {
            if(index>=0) {
                var price = obj.price
                var value = price[this.key_price[index]]

                try {
                    var str = value.replace(',', '')
                    eval(str)
                    this.$set(this.price_status, index, true)
                    obj.price_status[index] = true
                }
                catch {
                    this.$set(this.price_status, index, false)
                    obj.price_status[index] = false
                }
            }

            if(this.edit_list.indexOf(obj) === -1) {
                this.edit_list.push(obj)
            }
        },
        saveEditTable() {
            this.loading = true
            work_id_list = []
            for(item of this.edit_list) {
                var price_status = item.price_status.every(Boolean)
                if(! price_status) {
                    alert('Cannot save: Invalid format')
                    this.loading = false
                    return false
                }
                setObjectArray(item.detail)
                setObjectArray(item.price)

                work_id_list.push(item.id)
            }

            var params = {
                work_data_list: this.edit_list,
                work_id_list: work_id_list
            }
            api("/report/api/edit-price-list/", "POST", params).then((data) => {
                data.forEach(item => {
                    var expense_item = this.init_expense_list.find(expense => expense.work_order.id == item.id)
                    expense_item.work_order = item
                    expense_item.work_order.price_status = [true, true, true]
                })

                if(! this.driver_id) {
                    this.matchDriverReport()
                }

                this.calcTotalPriceList()
                this.edit_list = []
                this.loading = false

            })
        },
        // Filter
        filterReport() {
            this.filtered_expense_list = [...this.expense_list]
            var work_check_length = this.price_work_check.length
            var allowance_check_length = this.price_allowance_check.length

            if(this.all_customer && work_check_length == 2 && allowance_check_length == 2) {
                this.filter_mode = false
                $('#modalFilterReport').modal('hide')
                return false
            }
            else if(this.customer_selected.length == 0 || work_check_length == 0 || allowance_check_length == 0) {
                return false
            }

            var work_status = true
            var allowance_status = true

            if(work_check_length == 1) {
                var work_checked = this.price_work_check[0]
            }
            if(allowance_check_length == 1) {
                var allowance_checked = this.price_allowance_check[0]
            }

            this.filter_mode = true
            this.filtered_expense_list = this.expense_list.filter(report => {
                var work_order = report.work_order
                var price = work_order.price

                try {
                    if(work_check_length == 1) {
                        if(work_checked) {
                            work_status = ! ('work' in price) || eval(price.work) == 0
                        }
                        else {
                            work_status = 'work' in price && eval(price.work) != 0
                        }
                    }

                    if(allowance_check_length == 1) {
                        if(allowance_checked) {
                            allowance_status = (! ('allowance' in price) || eval(price.allowance) == 0) &&
                                                (! ('overnight' in price) || eval(price.overnight) == 0)
                        }
                        else {
                            allowance_status = ('allowance' in price && eval(price.allowance) != 0) ||
                                                ('overnight' in price && eval(price.overnight) != 0)
                        }
                    }
                }
                catch {
                    work_status = true
                    allowance_status = true
                }

                if("customer_name" in work_order.detail) {
                    var customer_status = this.customer_selected.includes(work_order.detail.customer_name)
                }
                else if(work_order.work_normal) {
                    var customer_status = this.customer_selected.includes(work_order.work_normal.principal.name)
                }
                else {
                    var customer_status = this.customer_selected.includes(work_order.work_agent_transport.principal.name)
                }

                return customer_status && work_status && allowance_status
            })

            $('#modalFilterReport').modal('hide')
        },
        clearFilter() {
            this.all_customer = true
            this.customer_selected = [...this.customer_list]

            this.price_work_check = [true, false]
            this.price_allowance_check = [true, false]

            this.filtered_expense_list = [...this.expense_list]
            this.filter_mode = false
        },
    }
})
