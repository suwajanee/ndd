var employee_page = new Vue( {
    
    el: '#employee-page',
    data: {
        employees: [],
        job: '',
        page: '',
        today: new Date(),
        date_compare: new Date(),

        emp_count: 0,
        officer_count: 0,
        driver_count: 0,
        mechanic_count: 0,
        not_active_count: 0,

        edit: false,

        modal_add_mode: true,
        input_required: false,
        emp_data: {
            job: '',
        },
        // month_list: [],

        // min_date: '',
        // max_date: '',

        // today: '',
        // year: '',
        // month: '',
        // date_from: '',
        // date_to: '',

        // mode: 'due',
        // edit: false, 
        // loading: false,

        // cheque_list: [],
        // total: 0,
        // due_total: 0,
        // accept_total: 0,

        // edit_data: [],
    },

    methods: {
        reload(job, page) {

            this.getEmployeeCount()

            if(! page) {
                this.getEmployees(job)
                this.date_compare.setDate(this.today.getDate() + 8)
            }
            else {
                this.page = page
                if(page == 'not_active') {
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
                this.mechanic_count = data.mechanic
                this.not_active_count = data.not_active
            })
        },
        
        getEmployees(job) {
            if(job) {
                this.job = job
                api("/employee/api/get-employee/", "POST", {job: job}).then((data) => {
                    this.employees = data
                    this.employeeDetail()
                })
            }
            else {
                this.job = ''
                api("/employee/api/get-employee/").then((data) => {
                    this.employees = data
                    this.employeeDetail()
                })
            }
        },
        getNotActiveEmployee(){
            this.job = ''
            api("/employee/api/get-not-active-employee/").then((data) => {
                this.employees = data
                this.employeeDetail()
            })
        },
        getEmployeeSalary(){
            this.job = ''
            api("/employee/api/get-employee-salary/").then((data) => {
                this.employees = data
            })
        },

        employeeDetail() {
            if(this.job == 'driver'){
                this.employees.forEach(function(emp) {
                    emp.employee.age = employee_page.calcAge(emp.employee.birth_date)
                    emp.employee.exp = employee_page.calcExp(emp.employee.hire_date)
                    if(emp.pat_pass_expired_date) {
                        emp.pat_expired = new Date(emp.pat_pass_expired_date)
                    }
                    else {
                        emp.pat_expired = ''
                    }

                })
            }
            else {
                this.employees.forEach(function(emp) {
                    emp.age = employee_page.calcAge(emp.birth_date)
                    if(employee_page.page == 'not_active'){
                        emp.exp = employee_page.calcExp(emp.hire_date, emp.detail.fire_date || '')
                    }
                    else {
                        emp.exp = employee_page.calcExp(emp.hire_date)
                    }
                })
            }
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

                return year + '/' + month
            }
        },

        employeeModal(emp, license, pat_expired) {
            if(emp) {
                this.modal_add_mode = false
                this.emp_data = {
                    first_name: emp.first_name,
                    last_name: emp.last_name,
                    birth_date: emp.birth_date,
                    tel: emp.detail.tel,
                    account: emp.detail.account,
                    hire_date: emp.hire_date,
                    job: emp.job.job_title,
                    license_type: license || '',
                    pat_pass_expired_date: pat_expired || '',
                    status: emp.status,
                    fire_date: emp.detail.fire_date || '',
                    age: emp.age || '',
                    exp: emp.exp || ''
                }
            }
            else {
                this.modal_add_mode = true
                this.emp_data = {
                    first_name: '',
                    last_name: '',
                    birth_date: '',
                    tel: '',
                    account: '',
                    hire_date: '',
                    job: this.job,
                    license_type: '',
                    pat_pass_expired_date: '',
                }
            }
        },

        addEmployees() {
            this.input_required = false
            if(this.emp_data.first_name == '' || this.emp_data.last_name == '' || this.emp_data.job == ''){
                this.input_required = true
                return false;
            }
            else {
                api("/employee/api/add-employee/", "POST", {emp_data: this.emp_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.job, this.page)
                        $('#modalEmployee').modal('hide');
                    }
                })
            }
        },


    }
})
