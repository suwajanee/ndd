var agent_transport_add = new Vue( {
    
    el: '#agent-transport-add',
    data: {
        search_principal: '',
        principals: [],
        shippers: [],
        principal_name: '',
        input_required: false,
        
        details: [{
            date: '',
            size: '',
            quantity: 1,
        }],
        agent_transport_add_form: {
            principal: '',
            shipper: '',
            agent: '',
            booking_no: '',
            work_type: 'ep',

            operation_type: '',
            price: 0,
            
            pickup_from: '',
            return_to: '',

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
            this.getAgentTransportPrincipals()
        },

        getAgentTransportPrincipals() {
            api("/customer/api/get-principals/", "POST", {work_type: 'agent-transport'}).then((data) => {
                this.principals = data
            })
        },

        getShipper(principal) {
            if(this.agent_transport_add_form.principal != principal.id) {
                this.agent_transport_add_form.shipper = ''
            }
            this.principal_name = principal.name
            this.agent_transport_add_form.principal = principal.id
            api("/customer/api/get-shippers/", "POST", {principal: principal.id}).then((data) => {
                this.shippers = data
            })
        },
        addDetail() {
            this.details.push({
                date: '',
                size: '',
                quantity: 1,
            })
        },
        deleteDetail(index) {
            this.details.splice(index,1)
        },

        currencyFormat() {
            this.agent_transport_add_form.price = parseFloat(this.agent_transport_add_form.price).toFixed(2);
        },

        saveAddAgentTransports() {
            this.input_required = false
            var form = this.$refs.addAgentTransportForm
            for(var i=0; i < form.elements.length; i++){
                if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                    this.input_required = true
                    return false;
                }
            }
            api("/agent-transport/api/save-add-agent-transports/", "POST", {agent_transports: this.agent_transport_add_form, details: this.details}).then((data) => {
                if(data == "Success") {
                    window.location.replace("/agent-transport");
                }
            })
        },

    }
})
