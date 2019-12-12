var daily_expense_page = new Vue ({

    el: '#daily-expense-page',
    data: {
        page: '',

        co: '',
        date: '',

        report_list: [],
    },

    methods: {
        reload(date, co) {
            this.date = date
            this.co = co

            this.getDailyExpense(date, co)
        },

        filterDate(){
            // console.log(2)
            // console.log(this.co)
            window.open("/transport-report/daily-expense/" + this.date + "/" + this.co, "_self")
        },

        getDailyExpense(date, co) {
            console.log(3)
            console.log(date)
            console.log(co)
            if(date && co) {
                api("/transport-report/api/get-daily-expense/", "POST", {date: date, co: co}).then((data) => {
                    this.date = data.date
                    this.report_list = data.work_expense
                    // console.log(data)
                    
                })
            }
            else {
                api("/transport-report/api/get-daily-expense/").then((data) => {
                    this.date = data.date
                    this.report_list = data.work_expense
                    // console.log(data)
                })
            }
        }
        
    }
})
