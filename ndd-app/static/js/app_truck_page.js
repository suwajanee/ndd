var truck_page = new Vue ({

    el: '#truck-page',
    data: {
        page: '',
        manufacturer_list: [],
        truck_list: [],
        chassis_list: [],

        date_compare: new Date(),

        drivers: [],

        truck_count: 0,
        chassis_count: 0,

        edit_table: false,
        edit_data: [],


    },

    methods: {
        reload(page) {
            this.page = page
            this.edit_data = []
            this.getTruckChassisCount()
            this.getDriver()
            this.getManufacturer()

            this.date_compare = new Date()
            this.date_compare.setDate(this.date_compare.getDate() + 8)
            
            if(page == 'truck') {
                this.getTruck()
            }
            else {
                this.getChassis()
            }
        },

        getTruckChassisCount() {
            api("/truck/api/get-truck-chassis-count/").then((data) => {
                this.truck_count = data.truck
                this.chassis_count = data.chassis
            })
        },
        getManufacturer() {
            api("/truck/api/get-manufacturer/", "POST", {category: this.page}).then((data) => {
                this.manufacturer_list = data
            })
        },
        getTruck() {
            api("/truck/api/get-truck").then((data) => {
                this.truck_list = data
                this.settingDetail()
            })
        },
        getChassis() {
            api("/truck/api/get-chassis").then((data) => {
                this.chassis_list = data
                this.settingDetail()
            })
        },
        getDriver() {
            api("/employee/api/get-employee/", "POST", {job: 'driver'}).then((data) => {
                this.drivers = data.driver
            })
        },
        settingDetail() {
            if(this.page == 'truck') {
                this.truck_list.forEach(function(truck) {
                    truck.tax_expired = new Date(truck.tax_expired_date)
                    truck.pat_expired = new Date(truck.pat_pass_expired_date)
                })
            }
            else {
                this.chassis_list.forEach(function(chassis) {
                    chassis.tax_expired = new Date(chassis.tax_expired_date)
                })
            }
        },

        editData(data) {
            if(this.edit_data.indexOf(data) === -1) {
                this.edit_data.push(data)
            }
        },
        editExpiredDate() {
            if(this.edit_data) {
                api("/truck/api/edit-expired-date/", "POST", {category: this.page, details: this.edit_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                    }
                })
            }
        }




    }
})
