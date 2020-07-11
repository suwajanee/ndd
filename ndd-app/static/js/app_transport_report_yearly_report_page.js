var yearly_report_page = new Vue ({
    el: '#yearly-report-page',
    data: {
        page: '',

        year: '',
        year_list: [],
        
        month_list: [],

        date_list: [],
    },
    methods: {
        reload(page, year) {
            this.page = page
            this.year = year

            this.month_list = _month

            this.getYear()
            this.getSummaryDate(year)
        },
        changeYear() {
            window.open("/report/" + this.page + "/" + this.year + "/", "_self")
        },
        selectDate(month, period) {
            var url = "/report/" + this.page + "/" + this.year + "/" + month
            if(period > 0) {
                url += "/" + period
            }
            window.open(url, "_self")
        },
        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },
        getSummaryDate(year) {
            api("/summary-date/api/get-summary-date/", "POST", {year: year}).then((data) => {
                if(data == 'Error') {
                    window.location.replace("/dashboard")
                    return false
                }
                this.date_list = data
            })
        }
    }
})
