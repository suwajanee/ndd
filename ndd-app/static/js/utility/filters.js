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
