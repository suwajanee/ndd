var summary_customer_custom = new Vue( {
    
    el: '#summary-customer-custom',
    data: {
        search_principal: '',

        principal_id: '',
        principal_name: '',
        principal_type: '',
        principals: [],
        customer_details: [],
        booking_field: {},
        summary_forms: [],

        form_action: 'add',
        form_title: 'Customer Custom',
        edit_customer: '',
        customer_setting_modal: {
            customer: {
                id: '',
                name: ''
            },
            sub_customer: '',
            customer_title: '',
            option: '',
            form: null,
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
            this.getForms()
            this.booking_field = booking_field_text
        },
        getPrincipals() {
            api("/customer/api/get-principals/").then((data) => {
                this.principals = data
            })
        },
        getForms(){
            api("/summary/api/get-form/").then((data) => {
                this.summary_forms = data
            })
        },

        getDetails(principal) {
            this.principal_id = principal.id
            this.principal_name = principal.name
            this.principal_type = principal.work_type
            api("/summary/api/get-customer-custom/", "POST", { customer: principal.id }).then((data) => {
                this.customer_details = data
            })
        },

        settingForm(index) {
            if(index >= 0){
                this.customer_setting_modal = Object.assign({}, this.customer_details[index])

                this.edit_customer = this.customer_setting_modal.sub_customer

                this.form_action = 'edit'
                this.form_title = 'Edit Customer Custom'
            }
            else{
                this.customer_setting_modal = {
                    customer: {
                        id: this.principal_id,
                        name: this.principal_name,
                    },
                    sub_customer: '',
                    customer_title: '',
                    option: '',
                    form: null,
                }
                this.form_action = 'add'
                this.form_title = 'Customer Custom'
            }
        },

        addCustomerSetting() {
            var setting_exist = this.customer_details.find(customer => 
                checkNull(customer.sub_customer).replace(/\s/g, "").toLowerCase() == checkNull(this.customer_setting_modal.sub_customer).replace(/\s/g, "").toLowerCase()
            )

            if(setting_exist) {
                alert("This setting is existing.")
            }
            else(
                api("/summary/api/add-customer-custom/", "POST", { customer: this.principal_id, customer_setting: this.customer_setting_modal }).then((data) => {
                    $('#modalCustomerCustom').modal('hide')
                    this.customer_details = data
                })
            )
        },

        editCustomerSetting() {
            var setting_exist = this.customer_details.find(customer => 
                checkNull(customer.sub_customer).replace(/\s/g, "").toLowerCase() == checkNull(this.customer_setting_modal.sub_customer).replace(/\s/g, "").toLowerCase()
            )

            if(setting_exist != null & this.edit_customer != this.customer_setting_modal.sub_customer) {
                alert("This setting is existing.")
            }
            else {
                api("/summary/api/edit-customer-custom/", "POST", { customer: this.principal_id, customer_setting: this.customer_setting_modal }).then((data) => {
                    $('#modalCustomerCustom').modal('hide')
                    this.customer_details = data
                })
            }
        },

        deleteCustomerSetting(customer_id, id) {
            if (confirm('Are you sure?')){
                api("/summary/api/delete-customer-custom/", "POST", { customer: customer_id, setting_id: id }).then((data) => {
                    this.customer_details = data
                })
            }
        },

    }
})
