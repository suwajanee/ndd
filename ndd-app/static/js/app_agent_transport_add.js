var agent_transport_add = new Vue( {
    
    el: '#agent-transport-add',
    data: {
        search_principal: '',
        principals: [],
        shippers: [],
        principal_name: '',
        input_required: false,
        quantity_warning: false,

        container_size_1: [],
        container_size_2: [],
        
        details: [{
            date: '',
            size: '',
            quantity: 1,
            container_input: false,
            container: [{
                container_1: '',
                container_2: ''
            }]
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

            detail: {},
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
            this.getContainerSize()
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
        getContainerSize() {
            api("/booking/api/get-container-size/").then((data) => {
                this.container_size_1 = data.num_1
                this.container_size_2 = data.num_2
            })
        },

        addDetail() {
            this.details.push({
                date: '',
                size: '',
                quantity: 1,
                container_input: false,
                container: [{
                    container_1: '',
                    container_2: ''
                }]
            })
        },
        deleteDetail(index) {
            this.details.splice(index,1)
        },

        addContainerDetail(index) {
            var containers = this.details[index].container
            if(containers.length < 150) {
                this.details[index].container.push({
                    container_1: '',
                    container_2: ''
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

        currencyFormat() {
            this.agent_transport_add_form.price = parseFloat(this.agent_transport_add_form.price).toFixed(2);
        },

        saveAddAgentTransports() {
            this.input_required = false
            this.quantity_warning = false
            var form = this.$refs.addAgentTransportForm
            for(var i=0; i < form.elements.length; i++){
                if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                    this.input_required = true
                }
            }

            this.details.forEach(function(detail) {
                if(detail.quantity < 1) {
                    agent_transport_add.quantity_warning = true
                }
                else if(detail.quantity > 150) {
                    agent_transport_add.quantity_warning = true
                }
            })

            if(this.input_required || this.quantity_warning) {
                return false
            }
            else {
                api("/agent-transport/api/save-add-agent-transports/", "POST", {agent_transports: this.agent_transport_add_form, details: this.details}).then((data) => {
                    if(data == "Success") {
                        window.location.replace("/agent-transport");
                    }
                })
            }
        },
    }
})
