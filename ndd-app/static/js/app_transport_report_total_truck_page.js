var total_truck_page = new Vue ({
    el: '#total-truck-page',
    data: {
        loading: false,
        copying: false,

        // Initial
        year: '',
        month: '',
        // End Initial

        // Upper Part
        year_list: [],
        month_list: [],
        full_month_list: [],
        // End Upper Part

        // Report Data
        from_date: '',
        to_date: '',
        // report list
        truck_list: [],
        list_count: 0,

        price_list: [],
        allowance_list: [],
        co_expense_list: [],

        total_list: [],
        // End Report Data
    },

    methods: {
        reload(year, month) {
            this.year = year
            this.month = month

            this.getYear()
            this.month_list = _month
            this.full_month_list = _full_month

            this.getTotalTruck()
        },

        getYear() {
            api("/summary/api/get-year/").then((data) => {
                this.year_list = data
            })
        },
        changeUrl() {
            var url = `/report/total-truck/${this.year}/${this.month}`
            window.open(url, "_self")
        },

        getTotalTruck() {
            this.loading = true
            api("/report/api/get-total-truck/", "POST", {year: this.year, month: this.month}).then((data) => {
                this.from_date = data.from_date
                this.to_date = data.to_date

                this.truck_list = data.truck
                this.list_count = this.truck_list.length

                this.price_list = this.addTotal(data.price)
                this.allowance_list = this.addTotal(data.allowance)
                this.co_expense_list = this.addTotal(data.co_expense)

                this.total_list = this.getTotalList()

                this.loading = false
            })
        },
        addTotal(arr) {
            arr.push(sumArray(arr))
            return arr
        },

        getTotalList() {
            total_list = []
            this.price_list.forEach((price, index) => {
                total_list.push(price - this.allowance_list[index] - this.co_expense_list[index])
            })
            return total_list
        },
        getPercentage(value, index) {
            var percentage = ((value / this.price_list[index]) * 100).toFixed(2)
            if(isNaN(percentage) || percentage.includes('Infinity')) {
                return '-'
            }
            return percentage
        },

        copyRow(total_list) {
            this.copying = true
            var list_len = total_list.length - 1
            var data = ""
            for(var i=0; i < list_len; i++) {
                data += total_list[i] + "\t\t"
            }
            copyToClipboard(data.trim())
            this.copying = false
        }

    },
})


