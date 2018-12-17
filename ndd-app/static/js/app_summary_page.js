var summary_page = new Vue( {
    
    el: '#summary-page',
    data: {
        year_summary: [],
        add_year:'',
        
    },

    computed: {
        
    },
    methods: {
        reload() {
            this.getSummaryYear()
        },
        getSummaryYear() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_summary = data
                for(year in this.year_summary){
                    this.year_summary[year].total = currencyCommas(this.year_summary[year].total)
                }
            })
        },


    }
})
