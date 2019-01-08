Vue.filter('formatDate', function(value) {
    if(value == null){
        return 
    }
    return dateFormat(value)
})

var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
function dateFormat(date) {
    var date = new Date(date)
    var date_num = date.getDate()
    var month = monthNames[date.getMonth()]
    var year = date.getFullYear().toString().substr(-2)
    return date_num + ' ' + month + ' ' + year

}


Vue.filter('currencyCommas', function(price) {
    // console.log(price)
    if(price == null || price == 0 || isNaN(price)){
        return '-'
    }
    price += '';
    var x = price.split('.');
    var x1 = x[0];
    var x2 = x[1];
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
     x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }

    if(x2 == null || x2 == '00'){
        return x1 + '.' + '00'
    }
    else if(x2.length == 1){
        return x1 + '.' + x2 + '0'
    }
    
    return x1 + '.' + x2
})
