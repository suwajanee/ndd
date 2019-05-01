var dashboard_page = new Vue( {
    
    el: '#dashboard-page',
    data: {
        year: '',

        booking_total: 0,
        booking_pending: 0,
        booking_completed: 0,
        booking_cancel: 0,
        booking_pending_width: 0,
        booking_completed_width: 0,

        agent_total: 0,
        agent_pending: 0,
        agent_completed: 0,
        agent_cancel: 0,
        agent_pending_width: 0,
        agent_completed_width: 0,

        weekly_works: {
            booking_pending: [],
            booking_completed: [],
            agent_pending: [],
            agent_completed: [],
        },

        yearly_income: [],

    },

    methods: {
        reload() {
            this.getBookingDailyWork()
            this.getAgentTransportDailyWork()
            this.weeklyWorkChart()
            this.yearlyIncomeChart()
        },
        getBookingDailyWork() {
            api("/booking/api/get-booking-daily-works/").then((data) => {
                this.booking_total = data.total
                this.booking_pending = data.pending
                this.booking_completed = data.completed
                this.booking_cancel = data.cancel

                var max = data.total + data.cancel
                
                this.booking_pending_width = this.progressWidth(this.booking_pending, max)
                this.booking_completed_width = this.progressWidth(this.booking_completed, max)
            })
        },
        getAgentTransportDailyWork() {
            api("/agent-transport/api/get-agent-transport-daily-works/").then((data) => {
                this.agent_total = data.total
                this.agent_pending = data.pending
                this.agent_completed = data.completed
                this.agent_cancel = data.cancel

                var max = data.total + data.cancel
                
                this.agent_pending_width = this.progressWidth(this.agent_pending, max)
                this.agent_completed_width = this.progressWidth(this.agent_completed, max)
            })
        },
        progressWidth(val, max) {
            return (val/max)*100
        },

        weeklyWorkChart() {
            api("/api/get-weekly-works/").then((data) => {
                this.weeklyDataPoints(data)

                var chart = new CanvasJS.Chart("chartWeeklyWork", {
                    animationEnabled: true,
                    theme: "light2",
                    title:{
                        text: "Weekly Works",
                        fontSize: 30,
                        // fontColor: "#695A42"
                    },
                    axisX: {
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
                    ]
                });
                chart.render();
            })
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

        yearlyIncomeChart() {
            api("/api/get-yearly-income/").then((data) => {
                this.year = data.year
                this.yearlyDataPoints(data)

                var chart = new CanvasJS.Chart("chartYearlyIncome", {
                    animationEnabled: true,
                    theme: "light2",
                    title:{
                        text: "Yearly Income - " + this.year,
                        fontSize: 30,
                    },
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
            })
        },
        yearlyDataPoints(data){
            for (var i = 0; i < 12; i++) {
                this.yearly_income.push({
                    x: new Date(this.year, i),
                    y: parseFloat(data.total[i])
                });
            } 
        },
    }
})

function toolTipContent(e) {
	var str = ""
	var total = 0

    str += "<span class='text-primary'><strong>"+ e.entries[0].dataPoint.x.toDateString() +"</strong></span><br/><hr class='m-1'>"
    str += "<span class='text-success'>" + e.entries[0].dataSeries.name + ":</span> <strong>" + e.entries[0].dataPoint.y + "</strong><br/>"
    str += "<span class='text-success'> " + e.entries[1].dataSeries.name + ":</span> <strong>" + e.entries[1].dataPoint.y + "</strong><br/>"
    str += "<span class='text-warning'> " + e.entries[2].dataSeries.name + ":</span> <strong>" + e.entries[2].dataPoint.y+"</strong><br/>"
    str += "<span class='text-warning'> " + e.entries[3].dataSeries.name + ":</span> <strong>" + e.entries[3].dataPoint.y+"</strong><br/>"
    total = e.entries[0].dataPoint.y + e.entries[1].dataPoint.y + e.entries[2].dataPoint.y + e.entries[3].dataPoint.y 
	str += "<hr class='m-1'><strong><span class='text-danger'><u>Total</u>:</span> " + total + "</strong>"
	return str
}