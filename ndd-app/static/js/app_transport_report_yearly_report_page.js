var yearly_report_page = new Vue ({
    el: '#yearly-report-page',
    data: {
        page_name: '',

        year: '',
        year_list: [],
        
        month_list: [],

        date_list: [],
    },
    methods: {
        reload(page_name, year) {
            this.page_name = page_name
            this.year = year

            this.month_list = _month

            this.getYear()
            this.getSummaryDate(year)
        },
        changeYear() {
            var url = `/report/${this.page_name}/${this.year}/`
            window.open(url, "_self")
        },
        selectDate(month, period) {
            var url =`/report/${this.page_name}/${this.year}/${month}`
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
