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
            api("/customer/api/get-customer-details/", "POST", {principal: principal_id}).then((data) => {
                this.shippers = data
                window.location.hash = principal_id
            })
        },

        addCustomer() {
            this.input_required = false
            if(this.add_customer_form.name === ''){
                event.preventDefault()
                this.input_required = true
                return false;
            }
            var customer_name = this.principals.find(principal => 
                principal.name.replace(/\s/g, "").toLowerCase() == this.add_customer_form.name.replace(/\s/g, "").toLowerCase() &
                principal.work_type == this.add_customer_form.work_type
            )
            if(customer_name) {
                event.preventDefault()
                alert("This customer name is existing.")
            }
            else{
                api("/customer/api/save-add-customer-details/", "POST", { customer: this.add_customer_form }).then((data) => {
                    this.getPrincipals(data)
                    $('#modalAddCustomer').modal('hide');
                    this.add_customer_form.name = ''
                    this.add_customer_form.work_type = 'normal'
                    
                })
                
            }
        },

    }
})
