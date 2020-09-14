var employee_page = new Vue( {
    
    el: '#employee-page',
    data: {
        employees: [],
        nested_employees: [],

        truck_list: [],

        job: '',
        page: '',
        date_compare: '',

        job_list: [],

        emp_count: 0,

        driver_start_index: 1,

        edit_table: false,
        edit_data: [],

        modal_add_mode: true,
        input_required: false,
        warning_truck_driver: false,

        check_truck_driver: '',
        emp_data: {},
        salary_data: {},
        salary_history: [],

    },
    methods: {
        reload(job, page) {

            this.getJobList()
            this.getTruckList()
            this.edit_data = []
            this.input_required = false

            if(! page) {
                this.getEmployees(job)
            }
            else {
                this.page = page
                if(page == 'former') {
                    this.getFormerEmployee()
                }
                else if(page == 'salary') {
                    this.getEmployeeSalary()
                }

            }
        },

        getJobList() {
            api("/employee/api/get-job/").then((data) => {
                this.job_list = data
                this.emp_count = sumObjectArray(data, 'count')
            })
        },
        getTruckList() {
            api("/truck-chassis/api/get-active-truck/").then((data) => {
                this.truck_list = data
            })
        },

        getEmployees(job) {
            if(job) {
                this.job = job
                api("/employee/api/get-employee/", "POST", {job: job}).then((data) => {
                    this.employees = data.other
                    this.nested_employees = data.driver
                    this.date_compare = data.date_compare
                })
            }
            else {
                this.job = ''
                api("/employee/api/get-employee/").then((data) => {
                    this.employees = data.other
                    this.nested_employees = data.driver

                    this.driver_start_index = this.employees.length + 1
                })
            }
        },
        getFormerEmployee() {
            api("/employee/api/get-former-employee/").then((data) => { 
                this.employees = data.other
                this.nested_employees = data.driver

                this.driver_start_index = this.employees.length + 1
            })
        },
        getEmployeeSalary(){
            api("/employee/api/get-employee-salary/").then((data) => {
                this.nested_employees = data
            })
        },

        calcAge(date) {
            this.emp_data.age = ''
            if(date) {
                var diff_month = diff_months(date)
                var year = Math.floor(diff_month / 12)

                this.emp_data.age = year
            }
        },
        calcExp(date1, date2) {
            this.emp_data.exp = ''
            if(date1) {
                if(date2) {
                    var diff_month = diff_months(date1, date2)
                }
                else {
                    var diff_month = diff_months(date1)
                }
                var year = Math.floor(diff_month / 12)
                var month = diff_month % 12

                this.emp_data.exp = year + 'Y' + month + 'M'
            }
        },

        employeeModal(emp, driver) {
            this.input_required = false
            this.warning_truck_driver = false
            if(emp) {
                this.modal_add_mode = false
                this.emp_data = {
                    id: emp.id,
                    name_title: emp.name_title,
                    first_name: emp.first_name,
                    last_name: emp.last_name,
                    birth_date: emp.birth_date,
                    tel: emp.detail.tel || '',
                    account: emp.detail.account || '',
                    hire_date: emp.hire_date,
                    job: emp.job.job_title,
                    status: emp.status,
                    fire_date: emp.detail.fire_date || '',
                    co: emp.co,
                }

                this.calcAge(emp.birth_date)
                this.calcExp(emp.hire_date, emp.detail.fire_date || '')
                if(driver) {
                    var truck = ''
                    if(driver.truck) {
                        truck = driver.truck.id
                    }
                    this.emp_data.driver_id = driver.id
                    this.emp_data.license_type = driver.license_type
                    this.emp_data.pat_pass_expired_date = driver.pat_pass_expired_date || ''
                    this.emp_data.truck = truck
                }
            }
            else {
                this.modal_add_mode = true
                this.emp_data = {
                    name_title: 'นาย',
                    first_name: '',
                    last_name: '',
                    birth_date: '',
                    tel: '',
                    account: '',
                    hire_date: '',
                    job: this.job,
                    license_type: '3',
                    pat_pass_expired_date: '',
                    truck: '',
                }
            }
        },
        checkTruckDriver(truck) {
            this.warning_truck_driver = false
            if(this.emp_data.truck) {
                api("/truck-chassis/api/check-truck-driver/", "POST", {truck_id: truck}).then((data) => {
                    this.check_truck_driver = data.driver
    
                    if(! this.check_truck_driver || this.emp_data.driver_id == this.check_truck_driver) {
                        this.warning_truck_driver = false
                    }
                    else {
                        this.warning_truck_driver = true
                    }
                })
            }
        },
        addEmployees() {
            this.input_required = false
            if(! this.emp_data.first_name.trim() || ! this.emp_data.last_name.trim() || ! this.emp_data.job || this.warning_truck_driver){
                this.input_required = true
                return false
            }
            else {
                api("/employee/api/add-employee/", "POST", {emp_data: this.emp_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.page)
                        $('#modalEmployee').modal('hide')
                    }
                })
            }
        },
        editEmployees() {
            this.input_required = false
            if(! this.emp_data.first_name.trim() || ! this.emp_data.last_name.trim() || this.warning_truck_driver || (this.emp_data.status == 't' && ! this.emp_data.fire_date)){
                this.input_required = true
                return false
            }
            else {
                api("/employee/api/edit-employee/", "POST", {emp_data: this.emp_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.page)
                        $('#modalEmployee').modal('hide')
                    }
                })
            }
        },
        editData(driver) {
            if(this.edit_data.indexOf(driver) === -1) {
                this.edit_data.push(driver)
            }
        },
        editPatExpiredDriver() {
            if(this.edit_data.length){
                api("/employee/api/edit-pat-expired-driver/", "POST", {job: this.job, drivers: this.edit_data}).then((data) => {
                    if(data) {
                        this.nested_employees = data.driver
                        this.edit_data = []
                    }
                })
            }
            this.edit_table = false
        },

        salaryModal(emp, salary) {
            this.input_required = false
            var emp_id = emp.id
            this.salary_data = {
                emp_id: emp_id,
                salary_id: salary.id,
                full_name: emp.full_name,
                account: emp.detail.account,
                old_salary: salary.salary,
                new_salary: '',
                edit_salary: false,
            }
            api("/employee/api/get-salary-history/", "POST", {emp_id: emp_id}).then((data) => {
                this.salary_history = data
            })
        },
        editSalary() {
            this.input_required = false
            if(isNaN(parseFloat(this.salary_data.new_salary))) {
                this.input_required = true
                return false
            }
            else if(parseFloat(this.salary_data.old_salary) == parseFloat(this.salary_data.new_salary) || this.salary_data.new_salary == '') {
                $('#modalEmployeeSalary').modal('hide')
                return false
            }
            else {
                api("/employee/api/edit-salary/", "POST", {emp_id: this.salary_data.emp_id, salary_id: this.salary_data.salary_id, new_salary: this.salary_data.new_salary}).then((data) => {
                    if(data) {
                        this.nested_employees = data
                        $('#modalEmployeeSalary').modal('hide')
                    }
                })
            }
        },
        deleteLatestSalary(id, old_id) {
            if(confirm('Are you sure?')) {
                api("/employee/api/delete-latest-salary/", "POST", {latest_id: id, old_id: old_id}).then((data) => {
                    if(data) {
                        this.nested_employees = data
                        $('#modalEmployeeSalary').modal('hide')
                    }
                })
            }
        },

        deleteEmployees(emp_id) {
            if (confirm('Are you sure?')){
                api("/employee/api/delete-employee/", "POST", {emp_id: emp_id}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.page)
                        $('#modalEmployee').modal('hide')
                    }
                })
            }
        },

    }
})
