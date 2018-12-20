var summary_year_details = new Vue( {
    
    el: '#summary-year-details',
    data: {
        summary_year_details: [],
        total_month: [],
        total_customer: [],
        total_year: 0
    },

    computed: {
        
    },

    methods: {
        reload(year) {
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
                this.total_customer[year_detail] = detail.reduce((a, b) => a + b, 0)
            }
        },
        totalYear(){
            this.total_year = this.total_month.reduce((a, b) => a + b, 0)
            this.total_year = currencyCommas(this.total_year)
        }
        


    }
})