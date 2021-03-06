var summary_chart = new Vue( {
    
    el: '#summary-chart',
    data: {
        search_principal: '',
        principal_name: '',
        principals: [],
        year: '',

        chart: '',
        dataPoints: [],
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
        reload(year) {
            this.getPrincipals()
            this.year = year
            this.summaryTotal()
        },
        getPrincipals() {
            api("/customer/api/get-principals/").then((data) => {
                this.principals = data
            })
        },

        summaryTotal() {
            this.dataPoints = []
            this.principal_name = ''
            this.chart = new CanvasJS.Chart("chartContainer", {
                height: 900,
                animationEnabled: true,
                exportEnabled: true,
                theme: "light2",
                title: {
                    text: "Summary " + this.year,
                    fontSize: 28,
                },
                axisX: {
                    labelFontSize: 12,
                    interval: 1,
                },
                axisY2: {
                    titleFontSize: 18,
                    labelFontSize: 12,
                    title: "drayage total"
                },
                data: [{
                    type: "bar",
                    axisYType: "secondary",
                    yValueFormatString: "#,###.##",
                    dataPoints: this.dataPoints
                }]
            })
            api("/summary/api/get-summary-year-data/", "POST", { year: this.year }).then((data) => {
                this.addDataBar(data)
                this.chart.render();
            })
        },
        addDataBar(data) {
            for (var i = 0; i < data.length; i++) {
                this.dataPoints.push({
                    label: data[i].customer,
                    y: parseFloat(data[i].total)
                });
            }        
        },

        cusomerTotal(customer) {
            this.dataPoints = []
            this.principal_name = customer.name
            this.chart = new CanvasJS.Chart("chartContainer", {
                animationEnabled: true,
                exportEnabled: true,
                theme: "light2",
                title:{
                    text: customer.name + ' ' + this.year,
                    fontSize: 28,
                },
                axisX: {
                    interval: 1,
                    intervalType: "month",
                    valueFormatString: "MMM YYYY",
                    labelFontSize: 12,
                },
                axisY:{
                    title: "drayage total",
                    titleFontSize: 18,
                    labelFontSize: 12,
                    includeZero: false,
                },
                data: [{        
                    type: "line",  
                    xValueFormatString: "MMM YYYY",
                    yValueFormatString: "#,###.##",    
                    dataPoints: this.dataPoints
                }]
            });
            api("/summary/api/get-summary-customer-data/", "POST", { year: this.year, customer_id: customer.id }).then((data) => {
                this.addDataLine(data)
                this.chart.render();
            })
        },
        addDataLine(data) {
            for (var i = 0; i < data.length; i++) {
                this.dataPoints.push({
                    x: new Date(this.year, i),
                    y: parseFloat(data[i])
                });
            }    
        },      
    }
})
