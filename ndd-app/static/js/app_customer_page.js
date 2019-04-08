var customer_page = new Vue( {
    
    el: '#customer-page',
    data: {
        search_principal: '',
        principals: [],
        customer: '',
        shippers: [],

        input_required: false,

        add_customer_form: {
            name: '',
            work_type: 'normal'
        },

        edit_customer_form: '',

        add_shipper_name: '',
        add_shipper_address: [{
            type: '',
            address: ''
        }],

        shipper_name: '',
        edit_shipper_form: '',
        edit_shipper_address: []
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
            this.getPrincipals()
            var hash = window.location.hash.slice(1)

            if(hash) {
                this.getPrincipals(parseInt(hash))
            }
        },

        getPrincipals(principal_id) {
            api("/customer/api/get-principals/").then((data) => {
                this.principals = data
                if ( principal_id ) {
                    this.getCustomerDetails(principal_id)
                }
            })
        },
        getCustomerDetails(principal_id) {
            window.location.hash = ''
            this.customer = this.principals.find(principal => principal.id == principal_id)
            this.edit_customer_form = Object.assign({}, this.customer)
            api("/customer/api/get-customer-details/", "POST", {principal: principal_id}).then((data) => {
                this.shippers = data
                window.location.hash = principal_id
            })

            this.add_shipper_name = ''
            this.add_shipper_address = [{
                type: '',
                address: ''
            }]
        },


        addCustomer() {
            this.input_required = false
            if(this.add_customer_form.name == ''){
                this.input_required = true
                return false;
            }
            var customer_name = this.principals.find(principal => 
                principal.name.replace(/\s/g, "").toLowerCase() == this.add_customer_form.name.replace(/\s/g, "").toLowerCase() &
                principal.work_type == this.add_customer_form.work_type
            )
            if(customer_name) {
                alert("This customer name is existing.")
            }
            else{
                api("/customer/api/save-add-customer/", "POST", { customer: this.add_customer_form }).then((data) => {
                    this.getPrincipals(data)
                    $('#modalAddCustomer').modal('hide');
                    this.add_customer_form.name = ''
                    this.add_customer_form.work_type = 'normal'   
                })
            }
        },
        editCustomer() {
            this.input_required = false

            if( this.edit_customer_form.name == this.customer.name & this.edit_customer_form.work_type == this.customer.work_type){
                $('#modalEditCustomer').modal('hide');
                return false
            }
            if(this.edit_customer_form.name == ''){
                this.input_required = true
                return false
            }
            var customer_name = this.principals.find(principal => 
                principal.name.replace(/\s/g, "").toLowerCase() == this.edit_customer_form.name.replace(/\s/g, "").toLowerCase() &
                principal.work_type == this.edit_customer_form.work_type
            )
            if(customer_name) {
                alert("This customer name is existing.")
            }
            else{
                api("/customer/api/save-edit-customer/", "POST", { customer: this.edit_customer_form }).then((data) => {
                    this.getPrincipals(data)
                    $('#modalEditCustomer').modal('hide');
                })
            }
        },
        cancelCustomer(customer_id, cancel_status) {
            api("/customer/api/cancel-customer/", "POST", { customer_id: customer_id, cancel_status: cancel_status }).then((data) => {
                this.getPrincipals(data)
            })
        },


        addShipperAddress(action) {
            if(action == 'add') {
                this.add_shipper_address.push({
                    type: '',
                    address: ''
                })
            }
            else if(action == 'edit') {
                this.edit_shipper_address.push({
                    type: '',
                    address: ''
                })
            }
        },
        deleteShipperAddress(index, action) {
            if(action == 'add') {
                this.add_shipper_address.splice(index,1)
            }
            else if(action == 'edit') {
                this.edit_shipper_address.splice(index,1)
            }
        },


        addShipper() {
            this.input_required = false
            if(this.add_shipper_name === ''){
                this.input_required = true
                return false;
            }
            var shipper_name = this.shippers.find(shipper => 
                shipper.shipper.name.replace(/\s/g, "").toLowerCase() == this.add_shipper_name.replace(/\s/g, "").toLowerCase()
            )
            if(shipper_name) {
                alert("This customer name is existing.")
            }
            else{
                api("/customer/api/save-add-shipper/", "POST", { customer_id: this.customer.id, shipper_name: this.add_shipper_name, address: this.add_shipper_address}).then((data) => {
                    this.getPrincipals(data)
                    $('#modalAddShipper').modal('hide');
                })
                this.add_shipper_name = ''
                this.add_shipper_address = [{
                    type: '',
                    address: ''
                }]  
            }
        },

        modalEditShipper(shipper_obj) {
            this.edit_shipper_address = []
            this.edit_shipper_form = {
                id: shipper_obj.id,
                name: shipper_obj.name
            }
            this.shipper_name = shipper_obj.name
            var address = this.shippers.filter(shipper => shipper.shipper.id == shipper_obj.id )
            if(address) {
                for(index in address) {
                    if(address[index].address || address[index].address_type) {
                        this.edit_shipper_address.push({
                            id: address[index].id,
                            type: address[index].address_type,
                            address: address[index].address
                        })
                    }
                }
            }
            this.edit_shipper_address.push({
                type: '',
                address: ''
            })
        },
        editShipper() {
            this.input_required = false

            if(this.edit_shipper_form.name === ''){
                this.input_required = true
                return false;
            }
            var shipper_name = this.shippers.find(shipper => 
                shipper.shipper.name.replace(/\s/g, "").toLowerCase() == this.edit_shipper_form.name.replace(/\s/g, "").toLowerCase()
            )

            if(shipper_name && this.edit_shipper_form.name != this.shipper_name) {
                alert("This customer name is existing.")
            }
            else{
                var address_id = this.edit_shipper_address.map(address => address.id);
                api("/customer/api/save-edit-shipper/", "POST", { shipper_detail: this.edit_shipper_form, shipper_address_detail: this.edit_shipper_address, address_id: address_id}).then(() => {
                    this.getPrincipals(this.customer.id)
                    $('#modalEditShipper').modal('hide');
                })
            }
        },

        cancelShipper(shipper_id, cancel_status) {
            api("/customer/api/cancel-shipper/", "POST", { shipper_id: shipper_id, cancel_status: cancel_status }).then(() => {
                this.getPrincipals(this.customer.id)
            })
        },

    }
})
