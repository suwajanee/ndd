var truck_page = new Vue ({

    el: '#truck-page',
    data: {
        page: '',
        truck_count: 0,
        chassis_count: 0,

        // Manufacturer
        truck_manu_list: [],
        chassis_manu_list: [],

        truck_manu_add: '',
        chassis_manu_add: '',
        truck_manu_add_warning: false,
        chassis_manu_add_warning: false,

        truck_manu_edit: [],
        chassis_manu_edit: [],
        truck_manu_edit_warning: [],
        chassis_manu_edit_warning: [],

        // Truck & Chassis
        truck_list: [],
        chassis_list: [],

        date_compare: '',

        edit_table: false,
        edit_list: [],
        
        modal_add_mode: true,
        input_required: false,
        modal_data: {},
    },

    methods: {
        reload(page) {
            this.page = page
            this.edit_list = []
            this.getTruckChassisCount()

            if(page == 'manufacturer') {
                this.getManufacturer(true)
            }
            else if(page == 'sold') {
                this.getSold()
            }
            else {
                this.getManufacturer(false)

                if(page == 'truck') {
                    this.getTruck()
                }
                else if(page == 'chassis') {
                    this.getChassis()
                }
            }
        },
        getTruckChassisCount() {
            api("/truck-chassis/api/get-truck-chassis-count/").then((data) => {
                this.truck_count = data.truck
                this.chassis_count = data.chassis
            })
        },

        // Manufacturer
        getManufacturer(init_manu_page) {
            api("/truck-chassis/api/get-manufacturer/").then((data) => {
                this.truck_manu_list = data.truck_manu
                this.chassis_manu_list = data.chassis_manu

                if(init_manu_page) {
                    this.truck_manu_edit = new Array(this.truck_manu_list.length)
                    this.truck_manu_edit.fill(false)
                    this.truck_manu_edit_warning = [...this.truck_manu_edit]

                    this.chassis_manu_edit = new Array(this.chassis_manu_list.length)
                    this.chassis_manu_edit.fill(false)
                    this.chassis_manu_edit_warning = [...this.chassis_manu_edit]
                }
            })
        },
        addManufacturer(category) {
            this[category + '_manu_add_warning'] = false
            var manu_add = this[category + '_manu_add']
            var name_exist = this[category + '_manu_list'].filter(manu => manu.name.toLowerCase().trim() == manu_add.toLowerCase().trim())
            if(! manu_add.trim() || name_exist.length > 0) {
                this[category + '_manu_add_warning'] = true
                return false
            }
            else {
                var data = {
                    name: manu_add,
                    category: category[0]
                }
                api("/truck-chassis/api/add-manufacturer/", "POST", data).then((data) => {
                    if(data == 'Success') {
                        this.getManufacturer(true)
                        this[category + '_manu_add'] = ''
                    }
                })
            }
        },
        editManuStatus(category, index) {
            this.$set(this[category + '_manu_edit_warning'], index, false)
            this.$set(this[category + '_manu_edit'], index, ! this[category + '_manu_edit'][index])
        },
        editManufacturer(category, index, manufacturer) {
            this.input_required = false
            var name_exist = this[category + '_manu_list'].filter(manu => 
                    (manu.name.toLowerCase().trim() == manufacturer.name.toLowerCase().trim()) && (manu.id != manufacturer.id)
                )
            if(! manufacturer.name.trim() || name_exist.length > 0) {
                this.$set(this[category + '_manu_edit_warning'], index, true)
                return false
            }
            else {
                api("/truck-chassis/api/edit-manufacturer/", "POST", {manufacturer: manufacturer}).then((data) => {
                    if(data == 'Success') {
                        this.getManufacturer(false)
                        this.editManuStatus(category, index)
                    }
                })
            }
        },
        deleteManufacturer(id) {
            if(confirm('Are you sure?')) {
                api("/truck-chassis/api/delete-manufacturer/", "POST", {id: id}).then((data) => {
                    if(data == 'Success') {
                        this.getManufacturer(true)
                    }
                })
            }
        },

        // Truck & Chassis
        getTruck() {
            api("/truck-chassis/api/get-truck/").then((data) => {
                this.truck_list = data.truck
                this.date_compare = data.date_compare
            })
        },
        getChassis() {
            api("/truck-chassis/api/get-chassis/").then((data) => {
                this.chassis_list = data.chassis
                this.date_compare = data.date_compare
            })
        },
        // Edit Date
        pushEditList(data) {
            if(this.edit_list.indexOf(data) === -1) {
                this.edit_list.push(data)
            }
        },
        editExpiredDate() {
            if(this.edit_list.length) {
                var category = this.page
                api("/truck-chassis/api/edit-expired-date/", "POST", {category: category, details: this.edit_list}).then((data) => {
                    this[category + '_list'] = data[category]
                    this.edit_list = []
                })
            }
            this.edit_table = false
        },
        // Add & Edit Popup
        modalTruckChassis(data) {
            this.input_required = false            
            if(data) {
                this.modal_add_mode = false
                var manufacturer = ''
                if(data.manufacturer) {
                    manufacturer = data.manufacturer.id
                }
                this.modal_data = {
                    id: data.id,
                    number: data.number,
                    license_plate: data.license_plate,
                    manufacturer: manufacturer,
                    tax_expired_date: data.tax_expired_date,

                    status: data.status
                }
                if(this.page == 'truck') {
                    this.modal_data.pat_pass_expired_date = data.pat_pass_expired_date
                }
            }
            else {
                this.modal_add_mode = true
                this.modal_data = {
                    number: '',
                    license_plate: '',
                    manufacturer: '',
                    
                    tax_expired_date: '',
                    pat_pass_expired_date: '',
                }
            }
        },
        actionTruckChassis(action) {
            this.input_required = false
            var category = this.page

            this.modal_data.number = this.modal_data.number.trim()
            var number_exist = this[category + '_list'].filter(item => 
                    (item.number.toLowerCase() == this.modal_data.number.toLowerCase()) && (item.id != this.modal_data.id)
                )
            if((! this.modal_data.number || number_exist.length > 0) && this.modal_data.status != 's') {
                this.input_required = true
                return false
            }
            else {
                var url = `/truck-chassis/api/${action}-${category}/`
                api(url, "POST", {data: this.modal_data}).then((data) => {
                    this[category + '_list'] = data[category]
                    this.getTruckChassisCount()
                    $('#modalTruckChassis').modal('hide')
                })
            }
        },

        // Sold
        getSold() {
            api("/truck-chassis/api/get-sold/").then((data) => {
                this.truck_list = data.truck
                this.chassis_list = data.chassis
            })
        },
        editStatus(category, id) {
            if(confirm('Are you sure?')) {
                var data = {
                    category: category,
                    id: id
                }
                api("/truck-chassis/api/edit-status/", "POST", data).then((data) => { 
                    this.truck_list = data.truck
                    this.chassis_list = data.chassis
    
                    this.getTruckChassisCount()
                })
            }
        },
    }
})
