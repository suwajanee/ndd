var agent_transport_table = new Vue( {
    
    el: '#agent-transport-table',
    data: {
        agent_transports: [],

        shippers: [],

        modal:'',
        shipper_address: [],

        checked_agent_transports: [],
        all_checked: false,

        filter_by: 'date',
        date_filter: '',

        nbar: 'table',
        
        booking_color: ['#9977b4', '#dd86b9', '#f497a9', '#f9b489', '#fdcd79', '#fff68f', '#b6d884', '#81cbb5', '#6acade', '#72abdd'],
        color_index: 0,
        action: '',
        
        edit_data: [],
        saving: false,
        loading: false,

        print: {
            template: '',
            address: '',
            address_other: ''
        }
        
    },

    methods: {
        reload() {
            if(localStorage.getItem('filter_by_agent_transport')){
                this.filter_by = localStorage.getItem('filter_by_agent_transport')
            }
            if(localStorage.getItem('date_filter_agent_transport')){
                this.date_filter = localStorage.getItem('date_filter_agent_transport')
            }

            var hash = window.location.hash.slice(1)
            if(hash == 'edit') {
                this.getAgentTransportsEditTable()
            }
            else {
                this.getAgentTransportsDataTable()
            }
        },

        getAgentTransportsDataTable() {
            this.filterAgentTransports()
            this.nbar = 'table'
        },
        getAgentTransportsEditTable() {
            window.location.hash = ''
            this.getShipper()
            this.filterAgentTransports()
            this.nbar = 'edit'
            window.location.hash = window.location.hash + 'edit'
        },

        filterAgentTransports() {
            this.loading = true
            this.checked_agent_transports = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            if(this.date_filter) {
                api("/agent-transport/api/filter-agent-transports/", "POST", {filter_by: this.filter_by, date_filter: this.date_filter}).then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                api("/agent-transport/api/filter-agent-transports/").then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.loading = false
                })
            }
            localStorage.setItem('filter_by_agent_transport', this.filter_by)
            localStorage.setItem('date_filter_agent_transport', this.date_filter)
        },

        getColor() {
            for(agent_transport in this.agent_transports) {

                if(agent_transport == 0){
                    this.agent_transports[agent_transport].color = this.booking_color[this.color_index=0]
                }
                else if(this.agent_transports[agent_transport].booking_no != this.agent_transports[agent_transport-1].booking_no){
                    this.agent_transports[agent_transport].color = this.booking_color[++this.color_index % 10]
                }
                else{
                    this.agent_transports[agent_transport].color = this.booking_color[this.color_index % 10]
                }

                if(! this.agent_transports[agent_transport].shipper){
                    this.agent_transports[agent_transport].shipper = 0
                }

            }
        },

        getShipper() {
            api("/customer/api/get-shippers/").then((data) => {
                this.shippers = data
            })
        },
        filterEditShipper(customer_id) {
            return this.shippers.filter(shipper => shipper.principal == customer_id )           
        },

        currencyCommas(price){
            price += '';
            var x = price.split('.');
            var x1 = x[0];
            var rgx = /(\d+)(\d{3})/;
            while (rgx.test(x1)) {
             x1 = x1.replace(rgx, '$1' + ',' + '$2');
            }
            return x1;
        },
        currencyFormat(index) {
            this.agent_transports[index].price = parseFloat(this.agent_transports[index].price).toFixed(2);
        },

        printFormModal(id, shipper_id) {
            this.modal = id
            this.shipper_address = []
            this.print.address_other = ''
            this.print.template = 'full'

            if(shipper_id == null) {
                this.print.address = 'other'
            }
            else{
                api("/customer/api/shipper-address/", "POST", {shipper_id: shipper_id}).then((data) => {
                    this.shipper_address = data
                    if(this.shipper_address.length) {
                        this.print.address = this.shipper_address[0].id
                    }
                    else {
                        this.print.address = 'other'
                    }
                })
            }
        },
        printSubmit(id) {
            this.$refs.printAgentTransportForm.action = "/agent-transport/print/" + id +"/"
            this.$refs.printAgentTransportForm.submit()
        },

        editData(agent_transport) {
            if(this.edit_data.indexOf(agent_transport) === -1) {
                this.edit_data.push(agent_transport)
            }
        },
        saveEditAgentTransport() {
            this.loading = true
            this.saving = true
            this.checked_agent_transports = []
            this.all_checked = false         
            if(this.edit_data.length) {
                api("/agent-transport/api/save-edit-agent-transports/", "POST", { agent_transports: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.edit_data = []
                    this.loading = false
                    this.saving = false
                })
            }
            else {
                this.loading = false
                this.saving = false
            }
        },

        selectAll() {
            this.checked_agent_transports = []

            if (!this.all_checked) {
                for (agent_transport in this.agent_transports) {
                    this.checked_agent_transports.push(this.agent_transports[agent_transport].id) 
                }
            }
        },
        selectAction() {
            if (! this.checked_agent_transports.length){
                alert('เลือกงานที่ต้องการ')
            }
            else if (this.action == 'delete'){
                if (confirm('Are you sure?')){
                    this.deleteAgentTransports()
                }
            }
            else {
                alert('Select action')
            }
        },

        deleteAgentTransports() {
            this.loading = true
            this.action = ''
            api("/agent-transport/api/delete-agent-transports/", "POST", { checked_agent_transports: this.checked_agent_transports, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                this.agent_transports = data.agent_transports
                this.getColor()

                this.loading = false
                this.checked_agent_transports = []
                this.all_checked = false
            })
        },

    }
})
