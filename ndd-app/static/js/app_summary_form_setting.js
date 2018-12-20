var summary_form_setting = new Vue( {
    
    el: '#summary-form-setting',
    data: {

        booking_field: {},
        create_new_form: {
            form_name: '',
            form_type: 'ndd',
            form_detail: ['0', 'none', 'remark', 'container_2', 'gate_charge'],
        },

        default_form: {
            form_name: '',
            form_type: 'ndd',
            form_detail: ['0', 'none', 'remark', 'gate_charge'],
        },

        form_title: 'Create New Form',
        button_label: 'Create',
        
        summary_form: [
            {
                form_name: 'Default',
                form_type: 'ndd',
                form_detail: ['0', 'ap_billing_no', 'remark', 'container_2', 'gate_charge']
            },
            {
                form_name: 'default2',
                form_type: 'ndd',
                form_detail: ['3', 'input_field', 'truck', 'date_from']
            },
            {
                form_name: 'default3',
                form_type: 'ndd',
                form_detail: ['2', 'diesel_rate', 'job_no', 'gate_charge']
            },
        ]
    },

    methods: {
        reload() {
            this.booking_field = booking_field_text
        },

        setting_form(index) {
            if(index >= 0){
                this.create_new_form = this.summary_form[index]
                this.button_label = 'Edit'
                this.form_title = 'Edit Form'
            }
            else{
                this.create_new_form = this.default_form
                this.button_label = 'Create'
                this.form_title = 'Create New Form'
            }
        }

    }
})
