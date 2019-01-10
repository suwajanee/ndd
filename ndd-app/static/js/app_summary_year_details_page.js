var summary_year_details = new Vue( {
    
    el: '#summary-year-details',
    data: {
        year: '',
        month: [],
        summary_year_details: [],
        total_month: [],
        total_customer: [],
        total_year: 0
    },

    methods: {
        reload(year) {
            this.year = year
            this.month = _month
            this.getSummaryYearDetails(year)
            
        },
        getSummaryYearDetails(year) {
            api("/summary/api/get-summary-year-details/", "POST", { year: year }).then((data) => {
                if(data == 'Error'){
                    window.location.replace("/summary")
                    return false
                }
                this.summary_year_details = data
                this.totalMonth()
                this.totalCustomer()
                this.totalYear()
                
            })
        },

        totalMonth(){
            for(year_detail in this.summary_year_details){
                var detail = this.summary_year_details[year_detail].total
                for(var i=0; i<12; i++){
                    if(year_detail == 0){
                        this.total_month[i] = 0
                    }
                    if(detail[i]){
                        this.total_month[i] += detail[i]
                    }
                }
            }
        },
        totalCustomer(){
            for(year_detail in this.summary_year_details){
                this.total_customer[year_detail] = 0
                var detail = this.summary_year_details[year_detail].total
                this.total_customer[year_detail] = sumArray(detail)
            }
        },
        totalYear(){
            this.total_year = sumArray(this.total_month)
        },

        selectMonth(month){
            window.location.replace("/summary/" + this.year + "/" + month)
        }

    }
})