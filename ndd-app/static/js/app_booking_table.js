var booking_table = new Vue( {
    
    el: '#booking-table',
    data: {
        bookings: [],
        today: '',
        tmr: '',

        shippers: [],

        modal:'',
        shipper_address: [],

        checked_bookings: [],
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
            this.filterBookings()
            this.nbar = 'table'
        },
        getBookingsEditTable() {
            window.location.hash = ''
            this.getShipper()
            this.filterBookings()
            this.nbar = 'edit'
            window.location.hash = window.location.hash + 'edit'
        },
        getBookingsTimeTable() {
            window.location.hash = ''
            this.filterTimeBookings()
            this.nbar = 'time'
            window.location.hash = window.location.hash + 'time'
        },

        filterBookings() {
            this.loading = true
            this.checked_bookings = []
            this.all_checked = false
            this.action = ''
            this.edit_data = []
            if(this.date_filter) {
                api("/booking/api/filter-bookings/", "POST", {filter_by: this.filter_by, date_filter: this.date_filter}).then((data) => {
                    this.bookings = data.bookings
                    this.today = data.today
                    this.tmr = data.tmr
                    this.getColor()
                    this.loading = false
                })
            }
            else {
                api("/booking/api/filter-bookings/").then((data) => {
                    this.bookings = data.bookings
                    this.today = data.today
                    this.tmr = data.tmr
                    this.getColor()
                    this.loading = false
                })
            }
            localStorage.setItem('filter_by_booking', this.filter_by)
            localStorage.setItem('date_filter_booking', this.date_filter)
        },

        getColor() {
            var num = 0
            for(booking in this.bookings) {

                var book = this.bookings[booking]

                if(booking == 0){
                    num = 1
                    book.color = this.booking_color[this.color_index=0]
                }
                else if(book.booking_no != this.bookings[booking-1].booking_no | book.date != this.bookings[booking-1].date){
                    num = 1
                    book.color = this.booking_color[++this.color_index % 10]
                }
                else{
                    num += 1
                    book.color = this.booking_color[this.color_index % 10]
                }

                book.num = num

                try {
                    var time = book.time.split('.')
                    if(parseInt(time[0])>0 & parseInt(time[0])<11){
                        book.timeColor = true
                    }
                    else{
                        book.timeColor = false
                    }
                }
                catch(err) {
                    book.timeColor = false
                }

                if(! book.detail || ! ('return_time' in book.detail)) {
                    this.$set(book, 'detail', {})
                }                

                if(! book.shipper){
                    book.shipper = 0
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
                if(((booking.nextday == '1' | booking.nextday == '2') & field == 22) | (booking.fac_ndd == '2' & field == 13)){
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
        saveEditBooking() {
            this.loading = true
            this.saving = true
            this.checked_bookings = []
            this.all_checked = false         
            if(this.edit_data.length) {
                api("/booking/api/save-edit-bookings/", "POST", { bookings: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                    this.bookings = data.bookings
                    this.today = data.today
                    this.tmr = data.tmr
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
        changeStateBooking(id, state) {
            api("/booking/api/change-state-booking/", "POST", {booking_id: id, state: state}).then((data) => {
                var booking = this.bookings.find(x => x.id == id)
                booking.status = data
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
            api("/booking/api/delete-bookings/", "POST", { checked_bookings: this.checked_bookings, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
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
                    this.today = data.today
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
                        this.today = data.today
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
                // if(! booking.hasOwnProperty("booking_time")) {
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
