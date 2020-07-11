var summary_date_page = new Vue ({
    el: '#summary-date-page',
    data: {
        year: '',
        year_list: [],
        month_list: [],

        date_list: [],

        modal_data: {},
        min_date: '',

    },

    methods: {
        reload(year) {
            this.year = year
            this.getSummaryDate(year)
            this.month_list = _month
            this.getYear()
        },
        changeUrl() {
            window.open("/summary-date/" + this.year + "/", "_self")
        },
        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },
        getSummaryDate(year) {
            api("/summary-date/api/get-summary-date/", "POST", {year: year}).then((data) => {
                if(data == 'Error'){
                    window.location.replace("/dashboard")
                    return false
                }
                this.date_list = data
            })
        },

        getModalSummaryDate(month, period, date, id) {
            this.modal_data = {
                pk: id,
                year: this.year,
                month: month,
                period: period,
                date: date
            }

            try {
                if(period==1) {
                    var before = this.date_list[month-1]
                    this.min_date = before[before.length-1].date
                }
                else {
                    this.min_date = this.date_list[month][period-2].date
                }
            }
            catch {
                this.min_date = ''
            }    
        },

        addSummaryDate() {
            if(this.modal_data.date) {
                api("/summary-date/api/add-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.date_list = data
                    }
                })
            }
            $('#modalSummaryDate').modal('hide')
        },

        updateSummaryDate() {
            if(this.modal_data.date) {
                api("/summary-date/api/edit-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.date_list = data
                    }
                })
            }
            else {
                api("/summary-date/api/delete-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.date_list = data
                    }
                })
            }
            $('#modalSummaryDate').modal('hide')
        },
    }
})
