var summary_month_details = new Vue( {
    
    el: '#summary-month-details',
    data: {
        year: '',
        month: '',
        month_list: [],
        year_list: [],

        weeks: [],

        summary_month_details: [],
        total_week: [],
        total_customer: [],
        total_month: 0,

        input_required: false,
        modal_action: 'add',
        summary_week_modal: {
            year: '',
            month: '',
            week: '',
            date_start: '',
            date_end: '',
            diesel_rate: ''
        }
    },

    computed: {

    },

    methods: {
        reload(year, month) {
            this.year = this.summary_week_modal.year = year
            this.month = this.summary_week_modal.month = month
            this.month_list = _month
            this.getSummaryMonthDetails(year, month)
            this.getYears()   
        },
        getSummaryMonthDetails(year, month) {
            api("/summary/api/get-summary-month-details/", "POST", { year: year, month: month }).then((data) => {
                if(data == 'Error'){
                    window.location.replace("/summary/" + this.year)
                    return false
                }
                this.summary_month_details = data.summary_month_details
                this.weeks = data.weeks

                this.totalWeek()
                this.totalCustomer()
                this.totalMonth()
                
            })
        },
        getYears() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_list = data
            })
        },

        totalWeek(){
            for(month_detail in this.summary_month_details){
                var detail = this.summary_month_details[month_detail].total
                for(week in this.weeks){
                    if(month_detail == 0){
                        this.total_week[week] = 0
                    }
                    if(detail[week]){
                        this.total_week[week] += detail[week]
                    }
                }
            }
        },
        totalCustomer(){
            for(month_detail in this.summary_month_details){
                this.total_customer[month_detail] = 0
                var detail = this.summary_month_details[month_detail].total
                this.total_customer[month_detail] = sumArray(detail)
            }
        },
        totalMonth(){
            this.total_month = sumArray(this.total_week)
        },

        selectWeek(week){
            window.location.replace("/summary/" + this.year + "/" + this.month + "/" + week)
        },

        addSummaryWeek() {

            this.input_required = false

            if(this.summary_week_modal.week == '' || this.summary_week_modal.date_start == '' || this.summary_week_modal.date_end == ''){
                this.input_required = true
                return false;
            }

            if(this.weeks){
                var week_exist = this.weeks.includes(this.summary_week_modal.week)
            }
            
            if(week_exist) {
                alert("This week is existing.")
            }
            else {
                api("/summary/api/add-summary-week/", "POST", { summary_week: this.summary_week_modal }).then((data) => {
                    $('#modalSummaryWeek').modal('hide')
                    this.getSummaryMonthDetails(this.year, this.month)                    
                })
            }
        },
        


    }
})