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
    return date_num+' '+month+' '+year

}


var booking_table = new Vue( {
    
    el: '#booking-table',
    
    data: {
        bookings: [],
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
        
        edit: [],
        loading: false,

        print: {
            template: '',
            address: '',
            address_other: ''
        }
        
    },

    // computed: {
    //     orderedBookings: function () {
    //         return _.orderBy(this.bookings, ['date', 'principal.name', 'shipper.name' ])
    //     }
    // },

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

            if(localStorage.getItem('nbar')){
                this.nbar = localStorage.getItem('nbar');
                if(this.nbar == 'table'){
                    this.getBookingsDataTable();
                }
                else if(this.nbar == 'edit'){
                    this.getBookingsEditTable();
                }
                else if(this.nbar == 'time'){
                    this.timeBookings();
                }
            }
            else{
                this.getBookingsDataTable();
            }
            
        },

        getBookingsDataTable() {
            this.loading = true;
            this.filterBookings();
            this.nbar = 'table';
            localStorage.setItem('nbar', this.nbar);
        },
        getBookingsEditTable() {
            this.loading = true;
            this.filterBookings();
            this.nbar = 'edit';
            localStorage.setItem('nbar', this.nbar);
        },
        timeBookings() {
            this.filterTimeBookings();
            this.nbar = 'time';
            localStorage.setItem('nbar', this.nbar);
        },

        filterBookings() {
            this.loading = true;
            this.checked_bookings = [];
            console.log(this.checked_bookings)
            this.all_checked = false;
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

        selectAll() {
            this.checked_bookings = []

            if (!this.all_checked) {
                for (booking in this.bookings) {
                    console.log('55555555')
                    this.checked_bookings.push(this.bookings[booking].id);   
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
            this.$refs.form.action = "/booking/print/" + id +"/"
            this.$refs.form.submit()

        },

        filterTimeBookings() {
            this.api("/booking/api/get-time-bookings/", "POST", {checked_bookings: this.checked_bookings}).then((data) => {
                this.bookings = data.bookings;
                this.getColor();
                this.splitTime()
            });           
        },

        splitTime() {
            for(booking in this.bookings) {
                try {
                var pickup_in_time = this.bookings[booking].pickup_in_time.split('//')
                console.log(pickup_in_time)
                this.bookings[booking].pickup_in__date = pickup_in_time[0]
                console.log(this.bookings[booking].pickup_in_date)
                this.bookings[booking].pickup_in__time = pickup_in_time[1]
                }
                catch{
                    this.bookings[booking].pickup_in__date = ''
                    this.bookings[booking].pickup_in__time = ''
                }
            }
        },

        selectAction() {
            if (this.checked_bookings.length == 0){
                alert('select?');
            }
            else if (this.action == 'delete'){
                if (confirm('Are you sure?')){
                    this.deleteBooking();
                }
            }
            else if (this.action == 'time') {
                this.timeBookings();
            }
            else {
                alert('Select action');
            }

        },

        ifChangeValue: function(booking) {
            if(this.edit.indexOf(booking) === -1) {
                this.edit.push(booking);
              }
        },

        editBooking: function() {
            this.loading = true;
            this.api("/booking/edit/", "POST", { booking: this.edit, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                this.bookings = data.bookings;
                this.getColor();
                this.loading = false;
            });
            
        },

        deleteBooking: function() {
            this.api("/booking/delete/", "POST", { pk: this.checked_bookings, filter_by: this.filter_by, date_filter: this.date_filter }).then((data) => {
                this.bookings = data.bookings;
                this.getColor();
            });
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
