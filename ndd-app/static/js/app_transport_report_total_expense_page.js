var total_expense_page = new Vue ({
    el: '#total-expense-page',
    data: {
        loading: false,

        // Initial
        year: '',
        month: '',
        period: '',
        // End Initial

        // Upper Part
        show_filter_btn: false,
        show_col_select: false,
        filter_mode: false,
        // option
        year_list: [],
        month_list: [],
        full_month_list: [],
        period_num: [],
        // End Upper Part

        // Report Data
        from_date: '',
        to_date: '',
        // report list
        total_report: [],
        date_list: [],
        // total
        thc_total_list: [],
        date_total_list: [],
        all_total_list: [],
        // End Report Data
    },
    methods: {
        reload(year, month, period) {
            this.year = year
            this.month = month
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
            var url = "/report/total-expense/" + this.year + "/" + this.month
            if (period > 0) {
                url += "/" + period
            }
            window.open(url, "_self")
        },

        getSummaryExpenseReport() {
            this.loading = true
            var filter = {
                year: this.year,
                month: this.month,
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
