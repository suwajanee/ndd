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

        edit_customer_form: ''


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
            this.edit_customer_form = this.customer
            api("/customer/api/get-customer-details/", "POST", {principal: principal_id}).then((data) => {
                this.shippers = data
                window.location.hash = principal_id
            })
        },

        addCustomer() {
            this.input_required = false
            if(this.add_customer_form.name === ''){
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

        // editCustomer() {
        //     this.input_required = false
        //     console.log(this.customer.name)
        //     console.log(this.edit_customer_form.name)
        //     if(this.edit_customer_form.name === this.customer.name & this.edit_customer_form.woke_type === this.customer.woke_type){
        //         $('#modalEditCustomer').modal('hide');
        //         console.log('11111111111111')
        //         return false
        //     }
        //     if(this.edit_customer_form.name === ''){
        //         this.input_required = true
        //         console.log('222222222222222')
        //         return false
        //     }
        //     var customer_name = this.principals.find(principal => 
        //         principal.name.replace(/\s/g, "").toLowerCase() == this.edit_customer_form.name.replace(/\s/g, "").toLowerCase() &
        //         principal.work_type == this.edit_customer_form.work_type
        //     )
        //     if(customer_name) {
        //         alert("This customer name is existing.")
        //     }
        //     else{
        //         api("/customer/api/save-edit-customer/", "POST", { customer: this.edit_customer_form }).then((data) => {
        //             this.getPrincipals(data)
        //             $('#modalEditCustomer').modal('hide');
        //         })
                
        //     }
        // },

    }
})
