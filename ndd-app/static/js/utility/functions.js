const api = (endpoint, method, data) => {
  var config = {
      method: method || 'GET',
      body: data !== undefined ? JSON.stringify(data) : null,
      headers: {
          'content-type': 'application/json'
      }
  }

  return fetch(endpoint, config)
      .then((response) => response.json())
      .catch((error) => console.log(error))
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
  else if(event.key == 'ArrowDown')
  {
      event.preventDefault()
      try {
          document.getElementById(field + '-' + down).focus()
      }
      catch(err){
      }
  }
  else if(event.key == 'ArrowRight')
  {
      event.preventDefault()
      try {
          document.getElementById(right + '-' + index).focus()
      }
      catch(err){
      }
  }
  else if(event.key == 'ArrowLeft')
  {
      event.preventDefault()
      try {
          document.getElementById(left + '-' + index).focus()
      }
      catch(err){
      }
  }
}

const currencyCommas = (price) => {
    price += '';
    var x = price.split('.');
    var x1 = x[0];
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
     x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    if(x[1] == '00'){
        return x1
    }
    return x1 + '.' + x[1];
}
