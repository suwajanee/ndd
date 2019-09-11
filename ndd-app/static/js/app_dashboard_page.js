var dashboard_page = new Vue( {
    
    el: '#dashboard-page',
    data: {
        year: '',
        date: '',
        year_list: [],
        principals: [],
        shippers: [],

        principal_id: '',

        booking_total: 0,
        booking_not_start: 0,
        booking_pending: 0,
        booking_completed: 0,
        booking_cancel: 0,
        booking_not_start_width: 0,
        booking_pending_width: 0,
        booking_completed_width: 0,

        agent_total: 0,
        agent_not_start: 0,
        agent_pending: 0,
        agent_completed: 0,
        agent_cancel: 0,
        agent_not_start_width: 0,
        agent_pending_width: 0,
        agent_completed_width: 0,

        truck_total: 0,
        truck_available: 0,
        truck_maintanance: 0,
        truck_available_width: 0,

        weekly_works: {
            booking_not_start: [],
            booking_pending: [],
            booking_completed: [],
            agent_not_start: [],
            agent_pending: [],
            agent_completed: [],
        },

        yearly_income: [],

    },

    methods: {
        reload() {
            this.getPrincipals()
            this.getYears()
            this.getBookingDailyWork()
            this.getAgentTransportDailyWork()
            this.getDailyTruck()
            this.weeklyWorkChart()
            this.yearlyIncomeChart()
        },
        getPrincipals() {
            api("/customer/api/get-principals/").then((data) => {
                this.principals = data
            })
        },
        getShipper(principal) {
            api("/customer/api/get-shippers/", "POST", {principal: principal}).then((data) => {
                this.shippers = data
            })
        },
        getYears() {
            api("/summary/api/get-summary-year/").then((data) => {
                this.year_list = data
                var this_year = new Date().getFullYear()
                var year_exist = this.year_list.find(x => x.year_label == this_year)
                if(! year_exist) {
                    this.year_list.unshift({year_label: this_year})
                }
            })
        },

        getBookingDailyWork() {
            api("/booking/api/get-booking-daily-works/").then((data) => {
                this.booking_total = data.total
                this.booking_not_start = data.not_start
                this.booking_pending = data.pending
                this.booking_completed = data.completed
                this.booking_cancel = data.cancel

                var max = data.total + data.cancel
                
                this.booking_not_start_width = this.progressWidth(this.booking_not_start, max)
                this.booking_pending_width = this.progressWidth(this.booking_pending, max)
                this.booking_completed_width = this.progressWidth(this.booking_completed, max)
            })
        },
        getAgentTransportDailyWork() {
            api("/agent-transport/api/get-agent-transport-daily-works/").then((data) => {
                this.agent_total = data.total
                this.agent_not_start = data.not_start
                this.agent_pending = data.pending
                this.agent_completed = data.completed
                this.agent_cancel = data.cancel

                var max = data.total + data.cancel
                
                this.agent_not_start_width = this.progressWidth(this.agent_not_start, max)
                this.agent_pending_width = this.progressWidth(this.agent_pending, max)
                this.agent_completed_width = this.progressWidth(this.agent_completed, max)
            })
        },
        getDailyTruck() {
            api("/truck/api/get-daily-trucks/").then((data) => {
                this.truck_total = data.total
                this.truck_available = data.available
                this.truck_maintanance = data.maintanance

                this.truck_available_width = this.progressWidth(this.truck_available, this.truck_total)
            })
        },
        progressWidth(val, max) {
            return (val/max)*100
        },

        weeklyWorkChart() {
            this.weekly_works = {
                booking_not_start: [],
                booking_pending: [],
                booking_completed: [],
                agent_not_start: [],
                agent_pending: [],
                agent_completed: [],
            }
            if(this.date) {
                api("/api/get-weekly-works/", "POST", { date: this.date }).then((data) => {
                    this.weeklyDataPoints(data.data_point)
                    this.createWorkChart()
                })
            }
            else {
                api("/api/get-weekly-works/").then((data) => {
                    this.weeklyDataPoints(data.data_point)
                    this.createWorkChart()
                })
            }
        },
        weeklyDataPoints(data){
            for (var key in data) {
                for (var i = 0; i < 7; i++) {
                    this.weekly_works[key].push({
                        x: new Date(data[key][i].x[0], data[key][i].x[1]-1, data[key][i].x[2]),
                        y: data[key][i].y
                    })
                }
            }
        },
        createWorkChart() {
            var chart = new CanvasJS.Chart("chartWeeklyWork", {
                animationEnabled: true,
                theme: "light2",
                axisX: {
                    stripLines: [
                        {
                            value: new Date(this.date).setHours(0, 0) || new Date().setHours(0, 0),
                            showOnTop: true,
                            color: '#007BFF'
                        }
                    ],
                    interval: 1,
                    valueFormatString: "DD MMM YY",
                    labelFontSize: 12,
                },
                axisY:{
                    gridColor: "lightgray",
                    tickColor: "lightgray",
                    labelFontSize: 12,
                },
                toolTip: {
                    shared: true,
                    content: toolTipContent
                },
                data: [{        
                        type: "stackedColumn",
                        showInLegend: true,
                        name: "Loading",
                        color: "LightGreen",
                        dataPoints: this.weekly_works.booking_completed
                    },
                    {        
                        type: "stackedColumn",
                        showInLegend: true,
                        name: "Agent",
                        color: "LightGreen",
                        dataPoints: this.weekly_works.agent_completed
                    },
                    {
                        type: "stackedColumn",
                        showInLegend: true,
                        color: "Khaki",
                        name: "Loading",
                        dataPoints: this.weekly_works.booking_pending
                    },
                    {        
                        type: "stackedColumn",
                        showInLegend: true,
                        name: "Agent",
                        color: "Khaki",
                        dataPoints: this.weekly_works.agent_pending
                    },
                    {
                        type: "stackedColumn",
                        showInLegend: true,
                        color: "Gainsboro",
                        name: "Loading",
                        dataPoints: this.weekly_works.booking_not_start
                    },
                    {        
                        type: "stackedColumn",
                        showInLegend: true,
                        name: "Agent",
                        color: "Gainsboro",
                        dataPoints: this.weekly_works.agent_not_start
                    },
                ]
            });
            chart.render();
        },

        yearlyIncomeChart() {
            this.yearly_income = []
            if(this.year) {
                api("/api/get-yearly-income/", "POST", { year: this.year }).then((data) => {
                    this.year = data.year
                    this.yearlyDataPoints(data)
                    this.createIncomeChart()
                })
            }
            else {
                api("/api/get-yearly-income/").then((data) => {
                    this.year = data.year
                    this.yearlyDataPoints(data)
                    this.createIncomeChart()
                })
            }
        },
        yearlyDataPoints(data){
            for (var i = 0; i < 12; i++) {
                this.yearly_income.push({
                    x: new Date(this.year, i),
                    y: parseFloat(data.total[i])
                });
            } 
        },
        createIncomeChart() {
            var chart = new CanvasJS.Chart("chartYearlyIncome", {
                animationEnabled: true,
                theme: "light2",
                axisX: {
                    interval: 1,
                    intervalType: "month",
                    valueFormatString: "MMM",
                    labelFontSize: 12,
                },
                axisY:{
                    gridColor: "lightgray",
                    tickColor: "lightgray",
                    labelFontSize: 12,
                    includeZero: false
                },
                data: [{        
                    type: "line",
                    color: "#007BFF",    
                    xValueFormatString: "MMM, YYYY",
                    yValueFormatString: "#,###.##", 
                    dataPoints: this.yearly_income
                }]
            })
            chart.render();
        },
    }
})

function toolTipContent(e) {
	var str = ""
	var total = 0

    str += "<span class='text-primary'><strong>"+ e.entries[0].dataPoint.x.toDateString() +"</strong></span><br/><hr class='m-1'>"
    str += "<span class='text-success'>" + e.entries[0].dataSeries.name + ":</span> <strong>" + e.entries[0].dataPoint.y + "</strong><br/>"
    str += "<span class='text-success'> " + e.entries[1].dataSeries.name + ":</span> <strong>" + e.entries[1].dataPoint.y + "</strong><br/>"
    str += "<span class='text-warning'> " + e.entries[2].dataSeries.name + ":</span> <strong>" + e.entries[2].dataPoint.y + "</strong><br/>"
    str += "<span class='text-warning'> " + e.entries[3].dataSeries.name + ":</span> <strong>" + e.entries[3].dataPoint.y + "</strong><br/>"
    str += "<span class='text-secondary'> " + e.entries[4].dataSeries.name + ":</span> <strong>" + e.entries[4].dataPoint.y + "</strong><br/>"
    str += "<span class='text-secondary'> " + e.entries[5].dataSeries.name + ":</span> <strong>" + e.entries[5].dataPoint.y + "</strong><br/>"
    total = e.entries[0].dataPoint.y + e.entries[1].dataPoint.y + e.entries[2].dataPoint.y + e.entries[3].dataPoint.y + e.entries[4].dataPoint.y + e.entries[5].dataPoint.y
    str += "<hr class='m-1'><strong><span class='text-danger'><u>Total</u>:</span> " + total + "</strong>"
    
	return str
}