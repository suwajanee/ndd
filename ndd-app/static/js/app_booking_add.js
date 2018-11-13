var booking_add = new Vue( {
    
    el: '#booking-add',
    data: {
        search_principal: '',
        principals: [],
        shippers: [],
        principal_name: '',
        input_required: false,
        
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

            nextday: false,
            return_date: '',

            closing_date: '',
            closing_time: '',
            remark: ''
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
            this.details[index].container.push({
                container_no: '',
                seal_no: ''
            })
            this.details[index].quantity += 1
        },
        deleteContainerDetail(index, index_cont) {
            this.details[index].container.splice(index_cont,1)
            this.details[index].quantity -= 1
        },

        containerCheck(index) {
            if(! this.details[index].container_input){
                this.details[index].quantity = this.details[index].container.length
            }
            else {
                this.details[index].quantity = this.details[index].container.length
            }
        },

        saveAddBookings() {
            this.input_required = false
            var form = this.$refs.addBookingForm
            for(var i=0; i < form.elements.length; i++){
                if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                    this.input_required = true
                    return false;
                }
            }
            api("/booking/api/save-add-bookings/", "POST", {bookings: this.booking_add_form, details: this.details}).then((data) => {
                if(data == "Success") {
                    window.location.replace("/booking");
                }
            })
        },

    }
})
