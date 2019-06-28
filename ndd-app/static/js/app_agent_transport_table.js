var agent_transport_table = new Vue( {
    
    el: '#agent-transport-table',
    data: {
        agent_transports: [],

        principals: [],
        shippers: [],
        shippers_list: [],

        modal:'',
        shipper_address: [],

        container_size_1: [],
        container_size_2: [],

        checked_agent_transports: [],
        all_checked: false,

        filter_by: 'date',
        date_filter: '',

        nbar: 'table',
        filter_mode: false,
        require_input: false,
        filter_data: {
            principal_id: '',
            shipper: '',
            booking_no: '',
            remark: '',
            date_from: '',
            date_to: '',
        },

        container_color: {},
        morning_color: {},
        
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
            this.container_color = container_seal_color
            this.morning_color = morning_color
            this.getContainerSize()
            this.getPrincipals()

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
            if(this.filter_mode) {
                this.filterAgentTransports()
            }
            else {
                this.getAgentTransports()
            }
            this.nbar = 'table'
            window.location.hash = ''
        },
        getAgentTransportsEditTable() {
            window.location.hash = ''
            this.getShipperList()
            if(this.filter_mode) {
                this.filterAgentTransports()
            }
            else {
                this.getAgentTransports()
            }
            this.nbar = 'edit'
            window.location.hash = window.location.hash + 'edit'
        },
        getContainerSize() {
            api("/booking/api/get-container-size/").then((data) => {
                this.container_size_1 = data.num_1
                this.container_size_2 = data.num_2
            })
        },
        getPrincipals() {
            api("/customer/api/get-principals/", "POST", {work_type: 'agent-transport'}).then((data) => {
                this.principals = data
            })
        },
        getShipper(principal) {
            if(! principal) {
                this.shippers = []
            }
            else {
                api("/customer/api/get-shippers/", "POST", {principal: principal}).then((data) => {	
                    this.shippers = data	
                })
            }	
        },

        getAgentTransports() {
            this.loading = true
            this.checked_agent_transports = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            this.filter_mode = false
            if(this.date_filter) {
                api("/agent-transport/api/get-agent-transports/", "POST", {filter_by: this.filter_by, date_filter: this.date_filter}).then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                api("/agent-transport/api/get-agent-transports/").then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.loading = false
                })
            }
            localStorage.setItem('filter_by_agent_transport', this.filter_by)
            localStorage.setItem('date_filter_agent_transport', this.date_filter)
        },
        filterAgentTransports() {
            this.require_input = false
            if(! this.filter_data.date_from || ! this.filter_data.date_to){
                this.require_input = true
                return false
            }
            this.loading = true
            this.checked_agent_transports = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            this.filter_mode = true
            if(this.filter_data.principal_id || this.filter_data.shipper || this.filter_data.booking_no || this.filter_data.remark || this.filter_data.date_from || this.filter_data.date_to) {
                api("/agent-transport/api/filter-agent-transports/", "POST", {filter_data: this.filter_data}).then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                this.getAgentTransports()
            }
        },
        clearFilterAgentTransports() {
            this.filter_data = {
                principal_id: '',
                shipper: '',
                booking_no: '',
                remark: '',
                date_from: '',
                date_to: '',
            }
            this.getAgentTransports()
        },

        getColor() {
            var num = 0

            for(agent_transport in this.agent_transports) {

                var agent = this.agent_transports[agent_transport]

                if(agent_transport == 0){
                    agent.color = this.booking_color[this.color_index=0]
                }
                else if(agent.booking_no != this.agent_transports[agent_transport-1].booking_no){
                    agent.color = this.booking_color[++this.color_index % 10]
                }
                else{
                    agent.color = this.booking_color[this.color_index % 10]
                }

                if(agent_transport == 0){
                    if(agent.status != '0') {
                        num = 1
                    }
                }
                else if(agent.date != this.agent_transports[agent_transport-1].date | agent.work_type != this.agent_transports[agent_transport-1].work_type | agent.shipper.id != this.agent_transports[agent_transport-1].shipper.id) {
                    if(agent.status != '0') {
                        num = 1
                    }
                }
                else {
                    if(agent.status != '0') {
                        num += 1      
                    }
                }

                if(agent.status != '0') {
                    agent.num = num
                }
                else {
                    agent.num = '-'
                }

                if(! agent.detail) {
                    this.$set(agent, 'detail', {})
                }  

                if(! agent.shipper){
                    agent.shipper = 0
                }

            }
        },

        getShipperList() {
            api("/customer/api/get-shippers/").then((data) => {
                this.shippers_list = data
            })
        },
        filterEditShipper(customer_id) {
            return this.shippers_list.filter(shipper => shipper.principal == customer_id )           
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

        editData(agent_transport, index, field) {
            if(index && field) {
                if(['1', '2'].includes(agent_transport.yard_ndd) & field == 10){
                    this.agent_transports[index].return_tr = ''
                }
            }

            if(this.edit_data.indexOf(agent_transport) === -1) {
                this.edit_data.push(agent_transport)
            }
        },
        editColorData: function(agent_transport) {
            if(agent_transport.detail.shipper_text_color) {
                if(agent_transport.detail.shipper_text_color == '#000000') {
                    agent_transport.detail.shipper_text_color = ''
                }
            }
            
            if(this.edit_data.indexOf(agent_transport) === -1) {
                this.edit_data.push(agent_transport)
            }            
        },
        saveEditAgentTransport() {       
            if(this.edit_data.length) {
                for(index in this.edit_data) {
                    var data = this.edit_data[index]
                    var shippers = this.filterEditShipper(data.principal.id)
                    if(! shippers.some(shipper => shipper.id == data.shipper.id)) {
                        alert('Fill in the Shipper')
                        return false
                    }
                }
                this.loading = true
                this.saving = true
                this.checked_agent_transports = []
                this.all_checked = false 
                api("/agent-transport/api/save-edit-agent-transports/", "POST", { agent_transports: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter, filter_mode: this.filter_mode, filter_data: this.filter_data }).then((data) => {
                    this.agent_transports = data.agent_transports
                    this.getColor()
                    this.edit_data = []
                    this.loading = false
                    this.saving = false
                })
            }
        },
        changeStateAgentTransport(id, state, status, color) {
            if(status && status == '2') {
                if(! color) {
                    color = 1
                }
                else {
                    color = (parseInt(color) + 1) % 3
                    if(color==0) { color = '' }
                }
                api("/agent-transport/api/change-color/", "POST", {id: id, color: color, field: 'morning_work'}).then((data) => {
                    var agent = this.agent_transports.find(x => x.id == id)
                    this.$set(agent.detail, 'morning_work', data)
                })
            }
            else {
                api("/agent-transport/api/change-state-agent-transport/", "POST", {agent_transport_id: id, state: state}).then((data) => {
                    var agent_transport = this.agent_transports.find(x => x.id == id)
                    agent_transport.status = data
                })
            }
        },
        checkColor(id, color, field) {
            if(! color) {
                color = 1
            }
            else {
                color = (parseInt(color) + 1) % 5
                if(color==0) { color = '' }
            }

            api("/agent-transport/api/change-color/", "POST", {id: id, color: color, field: field}).then((data) => {
                var agent = this.agent_transports.find(x => x.id == id)
                this.$set(agent.detail, field, data)
            })
        },
        checkPrint(id, color) {
            if(! color) {
                color = 1
            }
            else {
                color = ''
            }
            api("/agent-transport/api/change-color/", "POST", {id: id, color: color, field: 'print'}).then((data) => {
                var agent = this.agent_transports.find(x => x.id == id)
                this.$set(agent.detail, 'print', data)
            })
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
            api("/agent-transport/api/delete-agent-transports/", "POST", { checked_agent_transports: this.checked_agent_transports, filter_by: this.filter_by, date_filter: this.date_filter, filter_mode: this.filter_mode, filter_data: this.filter_data }).then((data) => {
                this.agent_transports = data.agent_transports
                this.getColor()

                this.loading = false
                this.checked_agent_transports = []
                this.all_checked = false
            })
        },

    }
})
