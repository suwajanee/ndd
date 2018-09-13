function updateradio(pk) {
    var address = document.getElementsByName("address"+pk);
    if (address[1].checked) {
        document.getElementById("id_address_other"+pk).disabled = false;
    } else {
        document.getElementById("id_address_other"+pk).disabled = true;
    }
}

function updateNextDay() {
    var nextday = document.getElementById("nextday");
    if (nextday.checked) {
        document.getElementById("id_return_date").disabled = false;
    } else {
        document.getElementById("id_return_date").disabled = true;
    }
}

function editNextDay(pk) {
    var nextday = document.getElementById("nextday"+pk);
    if (nextday.options[nextday.selectedIndex].value == '1') {
        document.getElementById("return_date"+pk).readOnly = false;
    } else {
        document.getElementById("return_date"+pk).readOnly = true;
    }
}

function changeDate(pk) {
    var nextday = document.getElementById("nextday"+pk);
    if (nextday.options[nextday.selectedIndex].value == '0') {
        document.getElementById("return_date"+pk).value = document.getElementById("date"+pk).value;
    }
}