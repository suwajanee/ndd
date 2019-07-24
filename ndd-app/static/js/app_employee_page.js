var employee_page = new Vue( {
    
    el: '#employee-page',
    data: {
        employees: [],
        job: '',
        today: new Date(),
        date_compare: new Date(),

        emp_count: 0,
        officer_count: 0,
        driver_count: 0,
        mechanic_count: 0,
        not_active_count: 0,

        edit: false,
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
                    this.employeeData()
                })
            }
            else {
                this.job = ''
                api("/employee/api/get-employee/").then((data) => {
                    this.employees = data
                    this.employeeData()
                })
            }
        },
        getNotActiveEmployee(){
            this.job = ''
            api("/employee/api/get-not-active-employee/").then((data) => {
                this.employees = data
            })
        },
        getEmployeeSalary(){
            this.job = ''
            api("/employee/api/get-employee-salary/").then((data) => {
                this.employees = data
            })
        },

        employeeData() {
            if(this.job == 'driver'){
                this.employees.forEach(function(emp) {
                    emp.age = employee_page.calcYear(emp.birth_date)
                    emp.work_period = employee_page.calcYear(emp.hire_date)
                    if(emp.pat_pass_expired_date) {
                        emp.pat_pass_expired_date = new Date(emp.pat_pass_expired_date)
                    }
                    else {
                        emp.pat_pass_expired_date = ''
                    }
                })
            }
            else {
                this.employees.forEach(function(emp) {
                    emp.age = employee_page.calcYear(emp.birth_date)
                    emp.work_period = employee_page.calcYear(emp.hire_date)
                })
            }
        },
        calcYear(date_string) {
            if(date_string) {
                var date = new Date(date_string)
                return Math.floor((Date.now() - date) / (31557600000))
            }
        }

    }
})
