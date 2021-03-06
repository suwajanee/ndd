var booking_add = new Vue( {
    
    el: '#booking-add',
    data: {
        search_principal: '',
        principals: [],
        shippers: [],
        principal_name: '',
        input_required: false,
        quantity_warning: false,

        container_size_1: [],
        container_size_2: [],
        
        nextday: false,
        details: [{
            date: '',
            time: '',
            size: '',
            quantity: 1,
            container_input: false,
            container: [{
                container_no: '',
                seal_no: ''
            }]
        }],
        booking_add_form: {
            principal: '',
            shipper: '',
            agent: '',
            booking_no: '',
            
            pickup_from: '',
            factory: '',
            return_to: '',
            vessel: '',
            port: '',

            nextday: '1',
            return_date: '',
            detail: {},

            closing_date: '',
            closing_time: '',
            remark: '',
            
        },
    },

    computed: {
        filteredPrincipal() {
            if(this.search_principal === '') return this.principals
            return this.principals.filter(principals => {
                return principals.name.toLowerCase().includes(this.search_principal.toLowerCase())
            })   
        }
    },
    methods: {
        reload() {
            this.getContainerSize()
            this.getBookingPrincipals()
        },

        getBookingPrincipals() {
            api("/customer/api/get-principals/", "POST", {work_type: 'normal'}).then((data) => {
                this.principals = data
            })
        },
        getShipper(principal) {
            if(this.booking_add_form.principal != principal.id) {
                this.booking_add_form.shipper = ''
            }
            this.principal_name = principal.name
            this.booking_add_form.principal = principal.id
            api("/customer/api/get-shippers/", "POST", {principal: principal.id}).then((data) => {
                this.shippers = data
            })
        },
        getContainerSize() {
            api("/booking/api/get-container-size/").then((data) => {
                this.container_size_1 = data.num_1
                this.container_size_2 = data.num_2
            })
        },

        addDetail() {
            this.details.push({
                date: '',
                time: '',
                size: '',
                quantity: 1,
                container_input: false,
                container: [{
                    container_no: '',
                    seal_no: ''
                }]
            })
        },
        deleteDetail(index) {
            this.details.splice(index,1)
        },

        addContainerDetail(index) {
            var containers = this.details[index].container
            if(containers.length < 150) {
                containers.push({
                    container_no: '',
                    seal_no: ''
                })
                this.details[index].quantity += 1
            }
        },
        deleteContainerDetail(index, index_cont) {
            this.details[index].container.splice(index_cont,1)
            this.details[index].quantity -= 1
        },

        containerCheck(index) {
            this.details[index].quantity = this.details[index].container.length
        },

        saveAddBookings() {
            this.input_required = false
            this.quantity_warning = false
            var form = this.$refs.addBookingForm
            for(var i=0; i < form.elements.length; i++){
                if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                    this.input_required = true
                }
            }

            this.details.forEach(function(detail) {
                if(detail.quantity < 1) {
                    booking_add.quantity_warning = true
                }
                else if(detail.quantity > 150) {
                    booking_add.quantity_warning = true
                }
            })

            if(this.input_required || this.quantity_warning) {
                return false
            }
            else {
                api("/booking/api/save-add-bookings/", "POST", {bookings: this.booking_add_form, details: this.details, nextday: this.nextday}).then((data) => {
                    if(data == "Success") {
                        window.location.replace("/booking");
                    }
                })
            }  
        },
    }
})
