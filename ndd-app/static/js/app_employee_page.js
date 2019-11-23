var employee_page = new Vue( {
    
    el: '#employee-page',
    data: {
        employees: [],
        drivers: [],

        truck_list: [],

        co: '',
        job: '',
        page: '',
        date_compare: '',

        emp_count: 0,
        officer_count: 0,
        driver_count: 0,
        sup_driver_count: 0,
        mechanic_count: 0,
        active_except_driver: 0,
        terminated_except_driver: 0,

        edit_table: false,
        edit_data: [],

        modal_add_mode: true,
        input_required: false,
        warning_truck_driver: false,

        check_truck_driver: '',
        emp_data: {
            job: '',
        },
        salary_data: {},
        salary_history: [],

    },

    methods: {
        reload(job, co, page) {

            this.getEmployeeCount()
            this.getTruckList()
            this.edit_data = []
            this.input_required = false

            this.co = co
            if(! page) {
                this.getEmployees(job)
            }
            else {
                this.page = page
                if(page == 'terminated') {
                    this.getNotActiveEmployee()
                }
                else if(page == 'salary') {
                    this.getEmployeeSalary()
                }

            }
        },
        getEmployeeCount() {
            api("/employee/api/get-employee-count/").then((data) => {
                this.emp_count = data.emp
                this.officer_count = data.officer
                this.driver_count = data.driver
                this.sup_driver_count = data.sup_driver
                this.mechanic_count = data.mechanic
                this.active_except_driver = data.active_except_driver
                this.terminated_except_driver = data.terminated_except_driver
            })
        },
        getTruckList() {
            api("/truck-chassis/api/get-truck/").then((data) => {
                this.truck_list = data.truck
            })
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
        
        getEmployees(job) {
            if(job) {
                this.job = job
                api("/employee/api/get-employee/", "POST", {job: job, co: this.co}).then((data) => {
                    this.employees = data.emp
                    this.drivers = data.driver
                    this.date_compare = data.date_compare
                })
            }
            else {
                this.job = ''
                api("/employee/api/get-employee/").then((data) => {
                    this.employees = data.emp
                    this.drivers = data.driver
                })
            }
        },
        getNotActiveEmployee(){
            this.job = ''
            api("/employee/api/get-not-active-employee/", "POST", {co: this.co}).then((data) => {
                this.employees = data.emp
                this.drivers = data.driver
            })
        },
        getEmployeeSalary(){
            this.job = ''
            api("/employee/api/get-employee-salary/", "POST", {co: this.co}).then((data) => {
                this.employees = data
            })
        },

        settingDetail() {
            this.drivers.forEach(function(driver) {
                driver.employee.age = employee_page.calcAge(driver.employee.birth_date)
                driver.employee.exp = employee_page.calcExp(driver.employee.hire_date)
            })

            this.employees.forEach(function(emp) {
                emp.age = employee_page.calcAge(emp.birth_date)
                if(employee_page.page == 'terminated'){
                    emp.exp = employee_page.calcExp(emp.hire_date, emp.detail.fire_date || '')
                }
                else {
                    emp.exp = employee_page.calcExp(emp.hire_date)
                }
            })
        },
        calcAge(date_string) {
            if(date_string) {
                var date = new Date(date_string)
                return Math.floor((Date.now() - date) / (31536000000))
            }
        },

        calcExp(date_string_1, date_string_2) {
            if(date_string_1) {
                var date_1 = new Date(date_string_1)
                if(date_string_2) {
                    var date_2 = new Date(date_string_2)
                    var diff_date = date_2 - date_1
                }
                else {
                    var diff_date = Date.now() - date_1
                }    
                var year =  Math.floor(diff_date / (31536000000))
                var month = Math.floor((diff_date % 31536000000)/2628000000)

                return year + 'y ' + month + 'm'
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

                    age: this.calcAge(emp.birth_date) || '',
                    exp: this.calcExp(emp.hire_date, emp.detail.fire_date || '') || ''
                }
                if(driver) {
                    var truck = ''
                    if(driver.truck) {
                        truck = driver.truck.id
                    }
                    this.emp_data.driver_id = driver.id
                    this.emp_data.license_type = driver.license_type
                    this.emp_data.pat_pass_expired_date = driver.pat_pass_expired_date || ''
                    this.emp_data.age = this.calcAge(driver.employee.birth_date) || ''
                    this.emp_data.exp = this.calcExp(driver.employee.hire_date, driver.employee.detail.fire_date || '') || ''

                    this.emp_data.truck = truck
                }
                // else {
                //     this.emp_data.age = this.calcAge(emp.birth_date) || ''
                //     this.emp_data.exp = this.calcExp(emp.hire_date, emp.detail.fire_date || '') || ''
                // }
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
                    co: this.co,
                    license_type: '3',
                    pat_pass_expired_date: '',
                    truck: '',
                }
            }
        },
        salaryModal(emp, salary) {
            this.input_required = false
            var emp_id = emp.id
            this.salary_data = {
                emp_id: emp_id,
                salary_id: salary.id,
                name_title: emp.name_title,
                first_name: emp.first_name,
                last_name: emp.last_name,
                account: emp.detail.account,
                old_salary: salary.salary,
                new_salary: '',
                edit_salary: false,
            }
            api("/employee/api/get-salary-history/", "POST", {emp_id: emp_id}).then((data) => {
                this.salary_history = data
            })
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
                        this.reload(this.job, this.co, this.page)
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
                        this.reload(this.job, this.co, this.page)
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
                api("/employee/api/edit-pat-expired-driver/", "POST", {drivers: this.edit_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.co, this.page)
                    }
                })
            }
            this.edit_table = false
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
                    if(data == 'Success') {
                        this.reload(this.job, this.co, this.page)
                        $('#modalEmployeeSalary').modal('hide')
                    }
                })
            }
        },

        deleteEmployees(emp_id) {
            if (confirm('Are you sure?')){
                api("/employee/api/delete-employee/", "POST", {emp_id: emp_id}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.co, this.page)
                        $('#modalEmployee').modal('hide')
                    }
                })
            }
        },


    }
})
