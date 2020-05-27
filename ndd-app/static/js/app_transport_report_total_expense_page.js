var total_expense_page = new Vue ({
    el: '#total-expense-page',
    data: {
        loading: false,

        year: '',
        month: '',
        period: '',
        co: '',

        from_date: '',
        to_date: '',

        year_list: [],
        month_list: [],
        full_month_list: [],
        period_num: [],

        total_report: [],
        date_list: [],

        thc_total_list: [],
        date_total_list: [],
        all_total_list: [],
    },
    methods: {
        reload(year, month, co, period) {
            this.year = year
            this.month = month
            this.co = co
            this.period = period

            this.getYear()
            this.month_list = _month
            this.full_month_list = _full_month

            this.getSummaryExpenseReport()
        },

        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },

        changeUrl(period) {
            if(period > 0) {
                window.open("/report/total-expense/" + this.year + "/" + this.month + "/" + this.co + "/" + period, "_self")
            }
            else {
                window.open("/report/total-expense/" + this.year + "/" + this.month + "/" + this.co, "_self")
            }
        },

        getSummaryExpenseReport() {
            this.loading = true
            var filter = {
                year: this.year,
                month: this.month,
                co: this.co,
                period: this.period
            }
            api("/report/api/get-total-expense/", "POST", filter).then((data) => {
                this.from_date = data.from_date
                this.to_date = data.to_date
                
                this.period_num = data.period

                this.total_report = data.total_report
                this.date_list = data.date

                this.thc_total_list = data.thc_total_list
                this.date_total_list = data.date_total_list
                this.all_total_list = data.all_total_list
                
                this.loading = false
            })
        }
    }
})
