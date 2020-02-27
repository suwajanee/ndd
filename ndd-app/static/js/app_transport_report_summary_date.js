var summary_date_page = new Vue ({
    el: '#summary-date-page',
    data: {
        year: '',
        year_list: [],
        month: [],
        ndd_list: [],
        vts_list: [],

        modal_data: {},
        min_date: '',

    },

    methods: {
        reload(year) {
            this.year = year
            this.getSummaryDate(year)
            this.month = _month
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
                this.ndd_list = data.ndd
                this.vts_list = data.vts 
            })
        },

        getModalSummaryDate(co, month, phase, date, id) {
            this.modal_data = {
                pk: id,
                year: this.year,
                month: month,
                phase: phase,
                co: co,
                date: date
            }

            try {
                if(co=='ndd') {
                    var co_list = this.ndd_list
                }
                else {
                    var co_list = this.vts_list
                }

                if(phase==1) {
                    var before = co_list[month-1]
                    this.date_min = before[before.length-1].date
                }
                else {
                    this.date_min = co_list[month][phase-2].date
                }
            }
            catch {
                this.date_min = ''
            }    
        },

        addSummaryDate() {
            if(this.modal_data.date) {
                api("/summary-date/api/add-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.ndd_list = data.ndd
                        this.vts_list = data.vts 

                    }
                })
            }
            $('#modalSummaryDate').modal('hide')
        },

        updateSummaryDate() {
            if(this.modal_data.date) {
                api("/summary-date/api/edit-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.ndd_list = data.ndd
                        this.vts_list = data.vts
                    }
                })
            }
            else {
                api("/summary-date/api/delete-summary-date/", "POST", this.modal_data).then((data) => {
                    if(data) {
                        this.ndd_list = data.ndd
                        this.vts_list = data.vts
                    }
                })
            }
            $('#modalSummaryDate').modal('hide')
        },
    }
})
