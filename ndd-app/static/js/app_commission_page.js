var commission_page = new Vue( {
    
    el: '#commission-page',
    data: {
        principals: [],

        search_principal: '',

        year_list: [],
        month_list: [],
        week_list: [],

        invoice_detail: [],

        // min_date: '',
        // max_date: '',

        // today: '',
        work: 'ndd',
        work_type: '',
        year: '',
        month: '',
        week: '',
        customer: '',
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
    computed: {
        filteredPrincipal() {
            if(this.search_principal === '') return this.principals
            return this.principals.filter(principals => {
                return principals.name.toLowerCase().includes(this.search_principal.toLowerCase())
            })   
        }
    },
    methods: {
        reload() {
            this.getAgentTransportPrincipals()
            this.getYears()
            this.month_list = _month

            var today = new Date()
            this.year = today.getUTCFullYear()
            this.month = today.getUTCMonth() + 1

            // this.getCheque()
        },

        getAgentTransportPrincipals() {
            api("/customer/api/get-principals/", "POST", {work_type: 'agent-transport'}).then((data) => {
                this.principals = data
            })
        },
        getYears() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_list = data
            })
        },
        getWeeks() {
            api("/summary/api/get-summary-weeks-by-month/", "POST", {year: this.year, month: this.month}).then((data) => {
                this.week_list = data
            })
        },

        getCommissionData(reset_week) {
            if(reset_week){
                this.week = ''
                this.getWeeks()
            }
            api("/summary/api/get-commission-data/", "POST", {year: this.year, month: this.month, week: this.week, customer: this.customer.id, work: this.work, work_type: this.work_type}).then((data) => {
                this.invoice_detail = data
            })
        },

        selectCustomer(customer) {
            
            this.customer = customer
            this.getCommissionData()

        }
       
    }
})
