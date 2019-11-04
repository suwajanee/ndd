var truck_page = new Vue ({

    el: '#truck-page',
    data: {
        page: '',
        owner_mode: '',

        truck_manu_list: [],
        chassis_manu_list: [],
        truck_list: [],
        chassis_list: [],

        date_compare: '',

        drivers: [],

        truck_count: 0,
        chassis_count: 0,
        sup_truck_count: 0,
        sup_chassis_count: 0,

        edit_table: false,
        edit_data: [],
        
        modal_truck_mode: '',
        modal_add_mode: true,
        input_required: false,

        truck_chassis_data: {},
        manufacturer_data: ''


    },

    methods: {
        reload(page, owner) {
            this.page = page
            this.edit_data = []
            this.getTruckChassisCount()
            this.getManufacturer()

            if(owner) {
                this.owner_mode = owner
            }
            
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
            api("/truck-chassis/api/get-truck-chassis-count/").then((data) => {
                this.truck_count = data.truck
                this.chassis_count = data.chassis
                this.sup_truck_count = data.sub_truck
                this.sup_chassis_count = data.sub_chassis
            })
        },
        getManufacturer() {
            api("/truck-chassis/api/get-manufacturer/").then((data) => {
                this.truck_manu_list = data.truck_manu
                this.chassis_manu_list = data.chassis_manu
            })
        },
        getTruck() {
            api("/truck-chassis/api/get-truck/", "POST", {owner: this.owner_mode}).then((data) => {
                this.truck_list = data.truck
                this.date_compare = data.date_compare
            })
        },
        getChassis() {
            api("/truck-chassis/api/get-chassis/", "POST", {owner: this.owner_mode}).then((data) => {
                this.chassis_list = data.chassis
                this.date_compare = data.date_compare
            })
        },
        getSold() {
            api("/truck-chassis/api/get-sold/", "POST", {owner: this.owner_mode}).then((data) => {
                this.truck_list = data.truck
                this.chassis_list = data.chassis
            })
        },

        editData(data) {
            if(this.edit_data.indexOf(data) === -1) {
                this.edit_data.push(data)
            }
        },
        editExpiredDate() {
            if(this.edit_data.length) {
                api("/truck-chassis/api/edit-expired-date/", "POST", {category: this.page, details: this.edit_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                    }
                })
            }
            this.edit_table = false
        },

        modalManufacturer(mode, data) {
            this.input_required = false
            if(data) {
                this.modal_add_mode = false
                this.manufacturer_data = {
                    id: data.id,
                    name: data.name,
                    category: mode
                }
            }
            else {
                this.modal_add_mode = true
                this.manufacturer_data = {
                    name: '',
                    category: mode
                }
            }
        },

        modalTruckChassis(mode, data) {
            this.input_required = false
            this.modal_truck_mode = mode
            if(data) {
                this.modal_add_mode = false
                var manufacturer = ''
                if(data.manufacturer) {
                    manufacturer = data.manufacturer.id
                }
                this.truck_chassis_data = {
                    id: data.id,
                    number: data.number,
                    license_plate: data.license_plate,
                    manufacturer: manufacturer,

                    tax_expired_date: data.tax_expired_date,

                    owner: data.owner,
                    status: data.status
                }
                if(mode) {
                    this.truck_chassis_data.pat_pass_expired_date = data.pat_pass_expired_date
                }
            }
            else {
                this.modal_add_mode = true
                this.truck_chassis_data = {
                    number: '',
                    license_plate: '',
                    manufacturer: '',
                    
                    tax_expired_date: '',
                    pat_pass_expired_date: '',

                    owner: this.owner_mode
                }
            }
        },
        addTruck() {
            this.input_required = false
            if(! this.truck_chassis_data.number.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/add-truck/", "POST", {truck: this.truck_chassis_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalTruckChassis').modal('hide')
                    }
                })
            }
        },
        addChassis() {
            this.input_required = false
            if(! this.truck_chassis_data.number.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/add-chassis/", "POST", {chassis: this.truck_chassis_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalTruckChassis').modal('hide')
                    }
                })
            }
        },
        addManufacturer() {
            this.input_required = false
            if(! this.manufacturer_data.name.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/add-manufacturer/", "POST", {manufacturer: this.manufacturer_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalManufacturer').modal('hide')
                    }
                })
            }
        },

        editTruck() {
            this.input_required = false
            if(! this.truck_chassis_data.number.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/edit-truck/", "POST", {truck: this.truck_chassis_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalTruckChassis').modal('hide')
                    }
                })
            }
        },
        editChassis() {
            this.input_required = false
            if(! this.truck_chassis_data.number.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/edit-chassis/", "POST", {chassis: this.truck_chassis_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalTruckChassis').modal('hide')
                    }
                })
            }
        },

        editManufacturer() {
            this.input_required = false
            if(! this.manufacturer_data.name.trim()) {
                this.input_required = true
                return false
            }
            else {
                api("/truck-chassis/api/edit-manufacturer/", "POST", {manufacturer: this.manufacturer_data}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalManufacturer').modal('hide')
                    }
                })
            }
        },

        deleteManufacturer(id) {
            if(confirm('Are you sure?')) {
                api("/truck-chassis/api/delete-manufacturer/", "POST", {id: id}).then((data) => {
                    if(data == 'Success') {
                        this.reload(this.page)
                        $('#modalManufacturer').modal('hide')
                    }
                })
            }
        }

        
      




    }
})
