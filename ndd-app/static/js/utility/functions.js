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
        try {
            document.getElementById(right + '-' + index).focus()
            event.preventDefault()
        }
        catch(err){
        }
    }
    else if(event.key == 'ArrowLeft') {
        try {
            document.getElementById(left + '-' + index).focus()
            event.preventDefault()
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

const sumString = (str) => {
    try {
        str = str.replace(',', '')
        return eval(str)
    }
    catch {
        return 0
    }
}

// รวม Object Array ที่ obj[key1] หรือ obj[key1][key2]
const sumObjectArray = (arr, key1, key2) => {
    if(arr){
        return arr.reduce((total, value) => {
            if(key2) {
                value = eval(value[key1][key2])
            }
            else {
                value = eval(value[key1])
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

// Copy to Clipboard
const copyToClipboard = (text) => {
    if(window.clipboardData && window.clipboardData.setData) {
        return clipboardData.setData("Test", text)
    }
    else if(document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea")
        textarea.textContent = text
        textarea.style.position = "fixed" // Prevent scrolling to bottom of page in MS Edge.
        document.body.appendChild(textarea)
        textarea.select()
        try {
            return document.execCommand("copy")
        } catch(ex) {
            console.warn("Copy to clipboard failed.", ex)
            alert("Copy failed")
            return false
        } finally {
            document.body.removeChild(textarea)
            alert("Copied")
        }

    }
}

// Remove unused key in object
const setObjectArray = (obj, number=false) => {
    Object.keys(obj).forEach(key => {
        if (obj[key]) {
            obj[key] = obj[key].trim()
            if (number) {
                obj[key] = obj[key].replace(',', '')
            }
        }
        else {
            delete obj[key]
        }
    })
    return obj
}

const diff_months = (dt1, dt2) => {
    var date1 = new Date(dt1)

    if(dt2) {
        var date2 = new Date(dt2)
    }
    else {
        var date2 = new Date()
    }
    var diff = (date2.getTime() - date1.getTime()) / 1000
    diff /= 2630880
    return Math.abs(Math.round(diff))
}

// Dropdown menu
const preventHideMenu = (id) => {
    var menu = document.getElementById(id)
    if(menu) {
        menu.addEventListener("click", function(e) {
            e.stopPropagation()
        })
    }
}

// Multiselect
const multiSelectAll = (app, input) => {
    if(app['all_' + input]) {
        app[input + '_selected'] = app[input + '_list']
    }
    else {
        app[input + '_selected'] = []
    }
}
const multiSelectCheck = (app, input) => {
    if(app[input + '_selected'].length == app[input + '_list'].length) {
        app['all_' + input] = true
    }
    else {
        app['all_' + input] = false
    }
}

// Clone Object (array) without ref
const cloneObject = (obj) => {
    return JSON.parse(JSON.stringify(obj))
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