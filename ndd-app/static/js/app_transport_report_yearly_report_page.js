var yearly_report_page = new Vue ({
    el: '#yearly-report-page',
    data: {
        page: '',

        year: '',
        year_list: [],
        
        month_list: [],

        ndd_list: [],
        vts_list: []
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
        selectDate(co, month, period) {
            var url = "/report/" + this.page + "/" + this.year + "/" + month + "/" + co
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
                this.ndd_list = data.ndd
                this.vts_list = data.vts
            })
        }
    }
})
