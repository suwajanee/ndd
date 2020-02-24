var cheque_page = new Vue( {
    
    el: '#cheque-page',
    data: {
        year_list: [],
        month_list: [],

        min_date: '',
        max_date: '',

        today: '',
        year: '',
        month: '',
        date_from: '',
        date_to: '',

        mode: 'due',
        edit: false,
        loading: false,

        cheque_list: [],
        total: 0,
        due_total: 0,
        accept_total: 0,

        edit_data: [],
    },

    methods: {
        reload() {
            this.getYears()
            this.month_list = _month

            var today = new Date()
            this.year = today.getUTCFullYear()
            this.month = today.getUTCMonth() + 1

            this.getCheque()
        },
        getYears() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },
        getCheque() {
            this.date_from = ''
            this.date_to = ''

            var last_day = new Date(this.year, this.month, 0).getDate()
            var month = (this.month<10?'0':'') + this.month
            this.min_date = this.year + '-' + month + '-01'
            this.max_date = this.year + '-' + month + '-' + last_day

            this.getChequeData(this.mode)
        },
        getChequeData(mode) {
            this.loading = true
            this.mode = mode
            api("/summary/api/get-cheque-data/", "POST", {year: this.year, month: this.month, date_from: this.date_from, date_to: this.date_to, mode: mode}).then((data) => {
                this.cheque_list = data.detail
                this.today = data.today
                this.due_total = data.due_total
                this.accept_total = data.accept_total

                this.totalCalc()
                this.loading = false 
            })
        },
        totalCalc() {
            var total = 0
            this.cheque_list.forEach(function(cheque) {
                total += parseFloat(cheque.total)
            })
            this.total = total
        },

        editData(cheque) {
            if(this.edit_data.indexOf(cheque) === -1) {
                this.edit_data.push(cheque)
            }
        },
        saveEditChequeAcceptDate() {
            if(this.edit_data.length){
                api("/summary/api/edit-cheque-accept-date/", "POST", { cheque_details: this.edit_data }).then((data) => {
                    this.getChequeData(this.mode)
                })
            }
            this.edit = false
        },
    }
})
