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
            api("/summary/api/get-summary-year/", "POST", {}).then((data) => {
                this.year_summary = data
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
                api("/summary/api/add-year/", "POST", { year: { year_label: this.add_year_input } }).then((data) => {
                    this.reload()
                    this.add_year_input = ''
                    $('#modalAddYear').modal('hide');  
                })
            }
        },


    }
})
