var summary_expense_page = new Vue ({
    el: '#summary-expense-page',
    data: {
        loading: false,

        year: '',
        month: '',
        period: '',
        co: '',
    },
    methods: {
        reload(year, month, co, period) {
            this.year = year
            this.month = month
            this.co = co
            this.period = period

            this.getSummaryExpenseReport()
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