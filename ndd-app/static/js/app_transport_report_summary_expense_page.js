var summary_expense_page = new Vue ({
    el: '#summary-expense-page',
    data: {
        loading: false,

        year: '',
        month: '',
        period: '',
        co: '',

        year_list: [],
        month_list: [],
        full_month_list: [],
        period_num: [],

        summary_list: [],
        date_list: [],
        thc_list: [],

        date_total_list: [],
        total_with_thc_list: [],
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
                window.open("/report/summary-expense/" + this.year + "/" + this.month + "/" + this.co + "/" + period, "_self")
            }
            else {
                window.open("/report/summary-expense/" + this.year + "/" + this.month + "/" + this.co, "_self")
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
            api("/report/api/get-summary-expense/", "POST", filter).then((data) => {
                console.log(data)
                this.period_num = data.period

                this.summary_list = data.summary
                this.date_list = data.date
                this.thc_list = data.thc

                this.date_total_list = data.date_total
                this.total_with_thc_list = data.total_with_thc
                
                this.loading = false
            })
        }
    }
})


// getExpenseReport() {
//     this.loading = true
//     var filter = {
//         year: this.year,
//         month: this.month,
//         co: this.co,
//         period: this.period
//     }
//     api("/report/api/get-expense-report/", "POST", filter).then((data) => {
//         this.report_list = data.expense
//         this.period_list = data.period

//         this.total_price_list = data.total[0]
//         this.total_expense_list = data.total[1]

//         this.pk_list = data.pk_list

//         this.customer_list = this.customer_selected = data.customer_list
//         this.remark_list = this.remark_selected = data.remark_list

//         this.loading = false
//     })
// },