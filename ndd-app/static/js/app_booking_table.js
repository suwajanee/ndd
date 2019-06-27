var booking_table = new Vue( {
    
    el: '#booking-table',
    data: {
        bookings: [],
        tmr: '',

        principals: [],
        shippers: [],
        shippers_list: [],

        modal:'',
        container_print_size: false,
        shipper_address: [],
        shipper_address_2: [],
        couple_error: false,

        container_size_1: [],
        container_size_2: [],

        checked_bookings: [],
        all_checked: false,

        filter_by: 'date',
        date_filter: '',

        nbar: 'table',
        filter_mode: false,
        filter_data: {
            principal_id: '',
            shipper: '',
            booking_no: '',
            remark: '',
            date_from: '',
            date_to: '',
        },
        
        container_color: {},
        time_color: {},
        morning_color: {},

        booking_color: ['#9977b4', '#dd86b9', '#f497a9', '#f9b489', '#fdcd79', '#fff68f', '#b6d884', '#81cbb5', '#6acade', '#72abdd'],
        color_index: 0,
        action: '',
        
        edit_data: [],
        saving: false,
        loading: false,

        print: {
            template: '',
            couple: false,
            work_with: '',
            address: '',
            address_other: '',
            couple_address: false,
            address_2: '',
            address_other_2: ''
        }
    },
    methods: {
        reload() {
            this.container_color = container_seal_color
            this.time_color = time_color
            this.morning_color = morning_color
            this.getContainerSize()
            this.getPrincipals()

            if(localStorage.getItem('filter_by_booking')){
                this.filter_by = localStorage.getItem('filter_by_booking')
            }
            if(localStorage.getItem('date_filter_booking')){
                this.date_filter = localStorage.getItem('date_filter_booking')
            }

            var hash = window.location.hash.slice(1)
            if(hash == 'edit') {
                this.getBookingsEditTable()
            }
            else if(hash == 'time') {
                this.getBookingsTimeTable()
            }
            else {
                this.getBookingsDataTable()
            }
        },

        getBookingsDataTable() {
            if(this.filter_mode) {
                this.filterBookings()
            }
            else {
                this.getBookings()
            }
            this.nbar = 'table'
            window.location.hash = ''
        },
        getBookingsEditTable() {
            window.location.hash = ''
            this.getShipperList()
            if(this.filter_mode) {
                this.filterBookings()
            }
            else {
                this.getBookings()
            }
            this.nbar = 'edit'
            window.location.hash = window.location.hash + 'edit'
        },
        getBookingsTimeTable() {
            window.location.hash = ''
            this.filterTimeBookings()
            this.nbar = 'time'
            window.location.hash = window.location.hash + 'time'
        },
        getContainerSize() {
            api("/booking/api/get-container-size/").then((data) => {
                this.container_size_1 = data.num_1
                this.container_size_2 = data.num_2
            })
        },
        getPrincipals() {
            api("/customer/api/get-principals/", "POST", {work_type: 'normal'}).then((data) => {
                this.principals = data
            })
        },
        getShipper(principal) {	
            api("/customer/api/get-shippers/", "POST", {principal: principal}).then((data) => {	
                this.shippers = data	
            })	
        },

        getBookings() {
            this.loading = true
            this.checked_bookings = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            this.filter_mode = false
            if(this.date_filter) {
                api("/booking/api/get-bookings/", "POST", {filter_by: this.filter_by, date_filter: this.date_filter}).then((data) => {
                    this.bookings = data.bookings
                    this.tmr = data.tmr
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                api("/booking/api/get-bookings/").then((data) => {
                    this.bookings = data.bookings
                    this.tmr = data.tmr
                    this.getColor()
                    this.loading = false
                })
            }
            localStorage.setItem('filter_by_booking', this.filter_by)
            localStorage.setItem('date_filter_booking', this.date_filter)
        },
        filterBookings() {
            this.loading = true
            this.checked_bookings = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            this.filter_mode = true
            if(this.filter_data.date_to) {
            }
            if(this.filter_data.principal_id || this.filter_data.shipper || this.filter_data.booking_no || this.filter_data.remark || this.filter_data.date_from || this.filter_data.date_to) {
                api("/booking/api/filter-bookings/", "POST", {filter_data: this.filter_data}).then((data) => {
                    this.bookings = data.bookings
                    this.tmr = data.tmr
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                this.getBookings()
            }
        },
        clearFilterBookings() {
            this.filter_data = {
                principal_id: '',
                shipper: '',
                booking_no: '',
                remark: '',
                date_from: '',
                date_to: '',
            }
            this.getBookings()
        },

        getColor() {
            var num = 0
            for(booking in this.bookings) {

                var book = this.bookings[booking]

                if(booking == 0){
                    if(book.status != '0') {
                        num = 1
                    }
                    book.color = this.booking_color[this.color_index=0]
                }
                else if(book.booking_no != this.bookings[booking-1].booking_no | book.date != this.bookings[booking-1].date){
                    if(book.status != '0') {
                        num = 1
                    }
                    book.color = this.booking_color[++this.color_index % 10]
                }
                else{
                    if(book.status != '0') {
                        num += 1
                    }
                    book.color = this.booking_color[this.color_index % 10]
                }

                if(book.status != '0') {
                    book.num = num
                }
                else {
                    book.num = '-'
                }

                try {
                    var time = book.time.split('.')
                    if(parseInt(time[0])>2 & parseInt(time[0])<10){
                        book.timeColor = true
                    }
                    else{
                        book.timeColor = false
                    }
                }
                catch(err) {
                    book.timeColor = false
                }

                if(! book.detail) {
                    this.$set(book, 'detail', {})
                }                

                if(! book.shipper){
                    book.shipper = 0
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

        printFormModal(id, shipper_id, size) {
            this.modal = id
            this.shipper_address = []
            this.couple_error = false

            this.print.address_other = ''
            this.print.couple = false
            this.print.work_with =  ''
            this.print.couple_address = false
            this.print.template = 'full'
            if(size.indexOf('20')) {
                this.container_print_size = true
            }
            else {
                this.container_print_size = false
            }

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
        getAddressFromWorkId(work_id) {
            this.couple_error = false
            api("/customer/api/shipper-address/", "POST", {work_id: work_id}).then((data) => {
                if(data == 'Error') {
                    this.couple_error = true
                    this.print.couple_address = false
                }
                else {
                    this.shipper_address_2 = data
                    this.print.couple_address = true
                    if(this.shipper_address_2.length) {
                        this.print.address_2 = this.shipper_address_2[0].id
                    }
                    else {
                        this.print.address_2 = 'other'
                    }
                }
            })
        },
        printSubmit(id) {
            this.couple_error = false
            if(this.print.couple) {
                api("/booking/api/check-work-id/", "POST", {work_id: this.print.work_with}).then((data) => {
                    if(data == 'Error') {
                        this.couple_error = true
                    }
                    else {
                        this.submitForm(id)
                    }
                })    
            }
            else {
                this.submitForm(id)
            }   
        },
        submitForm(id) {
            this.$refs.printBookingForm.action = "/booking/print/" + id +"/"
            this.$refs.printBookingForm.submit()
        },

        editData: function(booking, index, field) {
            if(index && field) {
                if(['1', '2'].includes(booking.yard_ndd) & field == 9){
                    this.bookings[index].forward_tr = ''
                    this.bookings[index].backward_tr = ''
                    this.bookings[index].return_tr = ''
                }
                if(((booking.nextday == '1' | (booking.nextday == '2')) & field == 22) | (booking.fac_ndd == '2' & field == 13)){
                    this.bookings[index].backward_tr = ''
                    this.bookings[index].return_tr = ''
                }
                if(['1', '3'].includes(booking.fac_ndd) & field == 13){
                    this.bookings[index].return_tr = ''
                }
            }
            
            if(this.edit_data.indexOf(booking) === -1) {
                this.edit_data.push(booking)
            }            
        },
        editColorData: function(booking) {
            if(booking.detail.shipper_text_color) {
                if(booking.detail.shipper_text_color == '#000000') {
                    booking.detail.shipper_text_color = ''
                }
            }
            
            if(this.edit_data.indexOf(booking) === -1) {
                this.edit_data.push(booking)
            }            
        },
        saveEditBooking() {
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
                this.checked_bookings = []
                this.all_checked = false 
                api("/booking/api/save-edit-bookings/", "POST", { bookings: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter, filter_mode: this.filter_mode, filter_data: this.filter_data }).then((data) => {
                    this.bookings = data.bookings
                    this.tmr = data.tmr
                    this.getColor()
                    this.edit_data = []
                    this.loading = false
                    this.saving = false
                })
            }
        },
        changeStateBooking(id, state, status, color) {
            if(status && status == '2') {
                if(! color) {
                    color = 1
                }
                else {
                    color = (parseInt(color) + 1) % 3
                    if(color==0) { color = '' }
                }
                api("/booking/api/change-color/", "POST", {id: id, color: color, field: 'morning_work'}).then((data) => {
                    var booking = this.bookings.find(x => x.id == id)
                    this.$set(booking.detail, 'morning_work', data)
                })
            }
            else {
                api("/booking/api/change-state-booking/", "POST", {booking_id: id, state: state}).then((data) => {
                    var booking = this.bookings.find(x => x.id == id)
                    booking.status = data
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

            api("/booking/api/change-color/", "POST", {id: id, color: color, field: field}).then((data) => {
                var booking = this.bookings.find(x => x.id == id)
                this.$set(booking.detail, field, data)
            })
        },
        checkPrint(id, color) {
            if(! color) {
                color = 1
            }
            else {
                color = ''
            }
            api("/booking/api/change-color/", "POST", {id: id, color: color, field: 'print'}).then((data) => {
                var booking = this.bookings.find(x => x.id == id)
                this.$set(booking.detail, 'print', data)
            })
        },

        selectAll() {
            this.checked_bookings = []

            if (!this.all_checked) {
                for (booking in this.bookings) {
                    this.checked_bookings.push(this.bookings[booking].id) 
                }
            }
        },
        selectAction() {
            if (! this.checked_bookings.length){
                alert('เลือกงานที่ต้องการ')
            }
            else if (this.action == 'delete'){
                if (confirm('Are you sure?')){
                    this.deleteBookings()
                }
            }
            else if (this.action == 'time') {
                this.getBookingsTimeTable()
            }
            else {
                alert('Select action')
            }
        },

        deleteBookings() {
            this.loading = true
            this.action = ''
            api("/booking/api/delete-bookings/", "POST", { checked_bookings: this.checked_bookings, filter_by: this.filter_by, date_filter: this.date_filter, filter_mode: this.filter_mode, filter_data: this.filter_data }).then((data) => {
                this.bookings = data.bookings
                this.getColor()

                this.loading = false
                this.checked_bookings = []
                this.all_checked = false
            })
        },

        filterTimeBookings() {
            this.loading = true
            this.edit_data = []
            if(this.checked_bookings.length) {
                api("/booking/api/get-time-bookings/", "POST", {checked_bookings: this.checked_bookings}).then((data) => {
                    this.bookings = data.bookings
                    this.tmr = data.tmr

                    this.getColor()

                    this.addTimeFields(data.booking_time)

                    this.loading = false
                })    
            }
            else {
                api("/booking/api/get-time-bookings/").then((data) => {
                    if(data == 'Not found') {
                        this.bookings = []
                        this.loading = false
                    }
                    else {
                        this.bookings = data.bookings
                        this.tmr = data.tmr

                        this.getColor()

                        this.addTimeFields(data.booking_time)

                        this.loading = false
                    }
                })    
            }      
        },
        addTimeFields(booking_time) {
            this.bookings.forEach(function(booking) {
                var time = booking_time.find(time => time.booking.id == booking.id)
                if(time) {
                    booking['booking_time'] = time
                }
                else {
                    booking['booking_time'] = {
                        pickup_in_time: {time: ''},
                        pickup_out_time: {time: ''},
                        factory_in_time: {time: ''},
                        factory_load_start_time: {time: ''},
                        factory_load_finish_time: {time: ''},
                        factory_out_time: {time: ''},
                        return_in_time: {time: ''},
                        return_out_time: {time: ''},
                    }
                }
            })
        },
        saveTimeBooking() {
            this.loading = true
            this.saving = true
            if(this.edit_data.length) {
                api("/booking/api/save-time-bookings/", "POST", { bookings: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter }).then(() => {
                    this.filterTimeBookings()
                    this.loading = false
                    this.saving = false
                })
            }
            else {
                this.loading = false
                this.saving = false
            }   
        },
    }
})
