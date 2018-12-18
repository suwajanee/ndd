var summary_page = new Vue( {
    
    el: '#summary-page',
    data: {
        year_summary: [],
        add_year_input:'',
        input_required: false
        
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
                    if(this.year_summary[year].total == null){
                        this.year_summary[year].total = '0.00'
                    }
                    else{
                        this.year_summary[year].total = currencyCommas(this.year_summary[year].total)
                    }    
                }
            })
        },
        addYear() {
            this.input_required = false
            if(this.add_year_input == ''){
                this.input_required = true
                return false;
            }
            var year_existing = this.year_summary.find(year => 
                year.year.replace(/\s/g, "").toLowerCase() == this.add_year_input.replace(/\s/g, "").toLowerCase()
            )
            if(year_existing) {
                alert("This year is existing.")
            }
            else{
                api("/summary/api/add-year/", "POST", { year: { name: this.add_year_input } }).then((data) => {
                    this.reload()
                    this.add_year_input = ''
                    $('#modalAddYear').modal('hide');  
                })
            }
        },


    }
})
