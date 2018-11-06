var customer_page = new Vue( {
    
    el: '#customer-page',
    data: {
        search_principal: '',
        principals: [],
        customer: '',
        shippers: []
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
                    this.getCustomerDetails(principal_id);  
                }
            })
        },
        getCustomerDetails(principal_id) {
            window.location.hash = ''
            this.customer = this.principals.find(principal => principal.id == principal_id);
            api("/customer/api/get-customer-details/", "POST", {principal: principal_id}).then((data) => {
                this.shippers = data
                window.location.hash = window.location.hash + principal_id
            })
        }

    }
})
