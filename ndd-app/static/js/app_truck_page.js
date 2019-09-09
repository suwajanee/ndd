var truck_page = new Vue ({

    el: '#truck-page',
    data: {
        page: '',
        manufacturer_list: [],
        truck_list: [],
        chassis_list: [],

        date_compare: '',

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
            
            if(page == 'truck') {
                this.getTruck()
            }
            else if(page == 'chassis') {
                this.getChassis()
            }
            else {
                this.getSold()
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
                this.truck_list = data.truck
                this.date_compare = data.date_compare
                // this.settingDetail()
            })
        },
        getChassis() {
            api("/truck/api/get-chassis").then((data) => {
                this.chassis_list = data.chassis
                this.date_compare = data.date_compare
            })
        },
        getSold() {
            api("/truck/api/get-sold").then((data) => {
                this.truck_list = data.truck
                this.chassis_list = data.chassis
                console.log(this.chassis_length)
            })
        },
        getDriver() {
            api("/employee/api/get-employee/", "POST", {job: 'driver'}).then((data) => {
                this.drivers = data.driver
            })
        },

        editData(data) {
            if(this.edit_data.indexOf(data) === -1) {
                this.edit_data.push(data)
            }
        },
        editExpiredDate() {
            if(this.edit_data.length) {
                api("/truck/api/edit-expired-date/", "POST", {category: this.page, details: this.edit_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                    }
                })
            }
            this.edit_table = false
        }




    }
})
