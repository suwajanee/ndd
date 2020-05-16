const api = (endpoint, method, data) => {
  var config = {
      method: method || 'GET',
      body: data !== undefined ? JSON.stringify(data) : null,
      headers: {
          'content-type': 'application/json'
      }
  }

    // return fetch(endpoint, config)
    //     .then((response) => response.json())
    //     .catch((error) => console.log(error))

return fetch(endpoint, config)
    .then((response) => response.json())
      .catch((error) => {throw Error(error);})
}


const keyDownArrow = (field, index) => {
    var up = index - 1
    var down = index + 1
    var right = field + 1
    var left = field - 1

    if(event.key == 'ArrowUp') {
        event.preventDefault()
        try {
            document.getElementById(field + '-' + up).focus()
        }
        catch(err){
        }
    }
    else if(event.key == 'ArrowDown' || event.keyCode == 13) {
        event.preventDefault()
        try {
            document.getElementById(field + '-' + down).focus()
        }
        catch(err){
        }
    }
    else if(event.key == 'ArrowRight') {
        event.preventDefault()
        try {
            document.getElementById(right + '-' + index).focus()
        }
        catch(err){
        }
    }
    else if(event.key == 'ArrowLeft') {
        event.preventDefault()
        try {
            document.getElementById(left + '-' + index).focus()
        }
        catch(err){
        }
    }
}

const arrayEqual = (arr1, arr2) => {
    return arr1.sort().toString() == arr2.sort().toString()
} 

const checkNull = (value) => {
    if(value){
        return value
    }
    return ''
}

// รวม Number Array
const sumArray = (arr) => {
    if(arr){
        return arr.reduce((a, b) => a + b, 0)
    }
    return
}

// รวม String Array
const sumStringArray = (arr) => {
    if(arr){
        return arr.reduce((a, b) => eval(a) + eval(b), 0)
    }
    return
}

// รวม Object Array ที่ obj[key1] หรือ obj[key1][key2]
const sumObjectArray = (arr, key1, key2) => {
    if(arr){
        return arr.reduce(function (total, value) {
            value = eval(value[key1])
            if(key2) {
                value = eval(value[key2])
            }
            if(! value) {
                value = 0
            }
            return total + value
        }, 0)
    }
    return
}

// Get day color row
const getDayColor = (date) => {
    var day_color = ['sun-color', 'mon-color', 'tue-color', 'wed-color', 'thu-color', 'fri-color', 'sat-color']
    date = new Date(date)
    var index = date.getDay()
    return day_color[index]
}

// Transport Report: Show/Hide note
const show_note = () => {
    var tbody = document.getElementById("tbody")
    tbody.addEventListener('mousedown', function(e) {
        e = e || window.event
        var target = e.target 
        var alert = target.children[0]
        if(alert && alert.tagName == "DIV" && target.tagName == "TD") {
            alert.style.display = "block"                   
        }
    }, false)  
}

const hide_note = () => {
    var tbody = document.getElementById("tbody")
    tbody.addEventListener('mouseup', function(e) {
        e = e || window.event
        var target = e.target
        var alert = target.children[0]
        if(alert && alert.tagName == "DIV" && target.tagName == "TD") {
            alert.style.display = "none"
        }
    }, false)
}

// Remove unused key in object
const remove_empty_key = (obj) => {
    // Object.keys(obj).forEach(key => ! obj[key] && delete obj[key])

    Object.keys(obj).forEach(key => {
        if(obj[key]) {
            obj[key] = obj[key].trim()
        }
        else {
            delete obj[key]
        }
    })

    return obj

}

var summary_breadcrumb = new Vue( {
    el: '#summary-breadcrumb',
    data: {
        month: '',
        month_list: [],
    },
    methods: {
        reload(month) {
            this.month = month
            this.month_list = _month
        },
    }
})