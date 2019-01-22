var summary_form_setting = new Vue( {
    
    el: '#summary-form-setting',
    data: {
        input_required: false,

        summary_forms: [],

        booking_field: {},
        form_action: 'create',
        form_title: 'Create New Form',
        form_id: '',
        form_setting_modal: {
            form_name: '',
            form_detail: ['00', '1_input_field', '2_remark', '4_gate_charge'],
        },
        form_index: -1,
        
        edit_form_name: '',
        edit_form_detail: []    
    },

    methods: {
        reload() {
            this.getForm()
            this.booking_field = booking_field_text
        },
        getForm(){
            api("/summary/api/get-form/").then((data) => {
                this.summary_forms = data
            })
        },

        settingForm(index) {
            if(index >= 0){
                this.form_id = this.summary_forms[index].id
                this.form_setting_modal.form_name = this.summary_forms[index].form_name
                this.form_setting_modal.form_detail = Array.from(this.summary_forms[index].form_detail)

                this.edit_form_name = this.form_setting_modal.form_name
                this.edit_form_detail = Array.from(this.form_setting_modal.form_detail)

                this.form_action = 'edit'
                this.form_title = 'Edit Form'
                this.form_index = index
            }
            else{
                this.form_setting_modal = {
                    form_name: '',
                    form_detail: ['00', '1_input_field', '2_remark', 'gate_charge'],
                }
                this.form_action = 'add'
                this.form_title = 'Create New Form'
                this.form_index = -1
            }
        },

        addForm() {
            this.input_required = false

            if(this.form_setting_modal.form_name == ''){
                this.input_required = true
                return false;
            }

            var form_exist = this.summary_forms.find(form => 
                form.form_name.replace(/\s/g, "").toLowerCase() == this.form_setting_modal.form_name.replace(/\s/g, "").toLowerCase() |
                arrayEqual(form.form_detail, this.form_setting_modal.form_detail)
            )

            if(form_exist) {
                alert("This form name is existing.")
            }
            else(
                api("/summary/api/add-form/", "POST", {form: this.form_setting_modal}).then((data) => {
                    $('#modalFormSetting').modal('hide')
                    this.summary_forms = data
                })
            )
        },

        editForm() {
            this.input_required = false

            if( this.edit_form_name == this.form_setting_modal.form_name & arrayEqual(this.edit_form_detail, this.form_setting_modal.form_detail)){
                $('#modalFormSetting').modal('hide');
                return false
            }

            if(this.form_setting_modal.form_name == ''){
                this.input_required = true
                return false
            }
            var form_name_exist = this.summary_forms.find(form => 
                form.form_name.replace(/\s/g, "").toLowerCase() == this.form_setting_modal.form_name.replace(/\s/g, "").toLowerCase()
            )
            var form_detail_exist = this.summary_forms.find(form => 
                arrayEqual(form.form_detail, this.form_setting_modal.form_detail)
            )

            if((form_name_exist != null & this.edit_form_name != this.form_setting_modal.form_name) |
                form_detail_exist != null & ! arrayEqual(this.edit_form_detail, this.form_setting_modal.form_detail)) {
                alert("This form name is existing.")
            }
            else {
                api("/summary/api/edit-form/", "POST", {form_id: this.form_id, form: this.form_setting_modal}).then((data) => {
                    $('#modalFormSetting').modal('hide')
                    this.summary_forms = data
                })
            }
        },

        deleteForm(id) {
            if (confirm('Are you sure?')){
                api("/summary/api/delete-form/", "POST", { form_id: id }).then((data) => {
                    this.summary_forms = data
                })
            }
        },
    }
})
