Vue.filter('formatDate', function(value) {
    if(value == null){
        return 
    }
    return dateFormat(value)
});

Vue.filter('split', function(value) {
    return value.split('//')
});

var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
function dateFormat(date) {
    var date = new Date(date)
    var date_num = date.getDate()
    var month = monthNames[date.getMonth()]
    var year = date.getFullYear().toString().substr(-2)
    return date_num + ' ' + month + ' ' + year

}


var booking_table = new Vue( {
    
    el: '#booking-table',
    
    data: {
        bookings: [],
        bookings_id: [],
        today: '',
        tmr: '',

        modal:'',
        shipper_address: '',

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
        api(endpoint, method, data) {
            var config = {
                method: method || 'GET',
                body: data !== undefined ? JSON.stringify(data) : null,
                headers: {
                    'content-type': 'application/json'
                }
            };

            return fetch(endpoint, config)
                .then((response) => response.json())
                .catch((error) => console.log(error));
        },
        reload() {
            if(localStorage.getItem('filter_by')){
                this.filter_by = localStorage.getItem('filter_by');
            }
            if(localStorage.getItem('date_filter')){
                this.date_filter = localStorage.getItem('date_filter');
            }
            this.getBookingsDataTable();
        },

        getBookingsDataTable() {
            this.filterBookings();
            this.nbar = 'table';
        },
        getBookingsEditTable() {
            this.filterBookings();
            this.nbar = 'edit';
        },
        getBookingsTimeTable() {
            this.filterTimeBookings();
            this.nbar = 'time';
        },

        filterBookings() {
            this.loading = true;
            this.checked_bookings = [];
            this.all_checked = false;
            this.action = ''
            this.edit_data = []
            if(this.date_filter) {
                this.api("/booking/api/filter-bookings/", "POST", {filter_by: this.filter_by, date_filter: this.date_filter}).then((data) => {
                    this.bookings = data.bookings
                    this.today = data.today
                    this.tmr = data.tmr
                    this.getColor();
                    this.loading = false;
                });
            }
            else {
                this.api("/booking/api/filter-bookings/").then((data) => {
                    this.bookings = data.bookings;
                    this.today = data.today
                    this.tmr = data.tmr
                    this.getColor();
                    this.loading = false
                });
            }
            localStorage.setItem('filter_by', this.filter_by);
            localStorage.setItem('date_filter', this.date_filter);
        },

        getColor() {
            for(booking in this.bookings) {

                if(booking == 0){
                    this.bookings[booking].color = this.booking_color[this.color_index=0]
                }
                else if(this.bookings[booking].booking_no != this.bookings[booking-1].booking_no){
                    this.bookings[booking].color = this.booking_color[++this.color_index % 10]
                }
                else{
                    this.bookings[booking].color = this.booking_color[this.color_index % 10]
                }

                try {
                    var time = this.bookings[booking].time.split('.')
                    if(parseInt(time[0])>0 & parseInt(time[0])<11){
                        this.bookings[booking].timeColor = true
                    }
                    else{
                        this.bookings[booking].timeColor = false
                    }
                }
                catch(err) {
                    this.bookings[booking].timeColor = false
                }
            }
        },

        printFormModal(id, shipper_id) {
            this.modal = id
            this.print.address_other = ''
            this.print.template = 'full'

            if(shipper_id == null) {
                this.print.address = 'other'
            }
            else{
                this.api("/customer/api/shipper-address/", "POST", {shipper_id: shipper_id}).then((data) => {
                    this.shipper_address = data
                    this.print.address = this.shipper_address[0].id
                });
            }
        },
        printSubmit(id) {
            this.$refs.printForm.action = "/booking/print/" + id +"/"
            this.$refs.printForm.submit()
        },

        editData: function(booking, index, field) {
            if(booking.yard_ndd == '1' & field == 9){
                this.bookings[index].forward_tr = ''
                this.bookings[index].backward_tr = ''
                this.bookings[index].return_tr = ''
            }
            if(booking.nextday == '1' & field == 22){
                this.bookings[index].backward_tr = ''
                this.bookings[index].return_tr = ''
            }
            if(booking.fac_ndd == '1' & field == 13){
                this.bookings[index].return_tr = ''
            }
            
            if(this.edit_data.indexOf(booking) === -1) {
                this.edit_data.push(booking);
            }
        },
        saveEditBooking: function() {
            this.loading = true;
            this.saving = true
            this.checked_bookings = [];
            this.all_checked = false;            
            if(this.edit_data.length > 0) {
                this.api("/booking/api/save-edit-bookings/", "POST", { bookings: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                    this.bookings = data.bookings
                    this.today = data.today
                    this.tmr = data.tmr

                    this.getColor();
                    this.edit_data = []
                    this.loading = false
                    this.saving = false
                });
            }
            else {
                this.loading = false
                this.saving = false
            }
        },

        selectAll() {
            this.checked_bookings = []

            if (!this.all_checked) {
                for (booking in this.bookings) {
                    this.checked_bookings.push(this.bookings[booking].id);   
                }
            }
        },
        selectAction() {
            if (this.checked_bookings.length == 0){
                alert('เลือกงานที่ต้องการ');
            }
            else if (this.action == 'delete'){
                if (confirm('Are you sure?')){
                    this.deleteBookings();
                }
            }
            else if (this.action == 'time') {
                this.getBookingsTimeTable();
            }
            else {
                alert('Select action');
            }
        },

        deleteBookings: function() {
            this.loading = true
            this.action = ''
            this.api("/booking/api/delete-bookings/", "POST", { checked_bookings: this.checked_bookings, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                this.bookings = data.bookings;
                this.getColor();

                this.loading = false
                this.checked_bookings = []
                this.all_checked = false;
            });
        },

        filterTimeBookings() {
            this.loading = true;
            this.edit_data = []
            this.api("/booking/api/get-time-bookings/", "POST", {checked_bookings: this.checked_bookings}).then((data) => {
                this.bookings = data.bookings;
                this.today = data.today
                this.tmr = data.tmr

                this.getColor();
                this.splitTime('pickup_in_time')
                this.splitTime('pickup_out_time')
                this.splitTime('factory_in_time')
                this.splitTime('factory_load_start_time')
                this.splitTime('factory_load_finish_time')
                this.splitTime('factory_out_time')
                this.splitTime('return_in_time')
                this.splitTime('return_out_time')
                this.loading = false;
            });           
        },
        splitTime(field) {
            for(booking in this.bookings) {
                if ( this.bookings[booking][field].indexOf('//') > -1 ) {
                    var pickup_in_time = this.bookings[booking][field].split('//')
                    this.bookings[booking][field + '__date'] = pickup_in_time[0]
                    this.bookings[booking][field + '__time'] = pickup_in_time[1]
                }
                else{
                    this.bookings[booking][field + '__date'] = ''
                    this.bookings[booking][field + '__time'] = ''
                }


            }
        },
        saveTimeBooking: function() {
            this.loading = true
            this.saving = true
            if(this.edit_data.length > 0) {
                this.api("/booking/api/save-time-bookings/", "POST", { bookings: this.edit_data, filter_by: this.filter_by, date_filter: this.date_filter }).then(() => {
                    this.filterTimeBookings()
                    this.loading = false
                    this.saving = false
                });
            }
            else {
                this.loading = false
                this.saving = false
            }   
        },
        printTime() {
            this.$refs.printTime.action = "/booking/time/print/"
            for(booking in this.bookings){
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = "pk_list";
                input.value = this.bookings[booking].id;
                this.$refs.printTime.appendChild(input)
            }
            this.$refs.printTime.submit()
        },

        keyDownArrow(field, index) {
            var up = index - 1
            var down = index + 1
            var right = field + 1
            var left = field - 1
            if(event.key == 'ArrowUp') {
                event.preventDefault();
                try {
                    document.getElementById(field + '-' + up).focus()
                }
                catch(err){
                }
            }
            else if(event.key == 'ArrowDown')
            {
                event.preventDefault();
                try {
                    document.getElementById(field + '-' + down).focus()
                }
                catch(err){
                }
            }
            else if(event.key == 'ArrowRight')
            {
                event.preventDefault();
                try {
                    document.getElementById(right + '-' + index).focus()
                }
                catch(err){
                }
            }
            else if(event.key == 'ArrowLeft')
            {
                event.preventDefault();
                try {
                    document.getElementById(left + '-' + index).focus()
                }
                catch(err){
                }
            }
        }
        
    }
});
