var expense_page = new Vue ({

    el: '#expense-page',
    data: {
        year: '',
        month: '',
        co: '',
        period: '',

        year_list: [],
        month_list: [],
        full_month_list: [],

        loading: false,

        col_price: true,
        col_allowance: true,
        col_remark: true,

        report_list: [],
        period_list: []
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

            this.getExpenseReport()
        },

        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },

        changeUrl(period) {
            if(period > 0) {
                window.open("/report/expense/" + this.year + "/" + this.month + "/" + this.co + "/" + period, "_self")
            }
            else {
                window.open("/report/expense/" + this.year + "/" + this.month + "/" + this.co, "_self")
            }
        },

        getExpenseReport() {
            var filter = {
                year: this.year,
                month: this.month,
                co: this.co,
                period: this.period
            }
            api("/report/api/get-expense-report/", "POST", filter).then((data) => {
                this.report_list = data.expense
                this.period_list = data.period
                console.log(data.pk_list)
                console.log(data.work_list)
                console.log(data.remark_list)
                console.log(data.customer_list)
            })
        }

        
    }
})