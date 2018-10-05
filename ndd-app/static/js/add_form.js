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
        document.getElementById("backward_tr"+pk).readOnly = false;
        document.getElementById('backward_tr'+pk).value = ''
        document.getElementById('return_tr'+pk).value = ''
    } else {
        document.getElementById("return_date"+pk).readOnly = true;
        document.getElementById("backward_tr"+pk).readOnly = true;
    }
}

function changeDate(pk) {
    var nextday = document.getElementById("nextday"+pk);
    if (nextday.options[nextday.selectedIndex].value == '0') {
        document.getElementById("return_date"+pk).value = document.getElementById("date"+pk).value;
    }
}


function editTrForward(pk) {
    var yard_ndd = document.getElementById("yard_ndd"+pk);
    if (yard_ndd.options[yard_ndd.selectedIndex].value == '1') {
        document.getElementById("forward_tr"+pk).readOnly = false;
        document.getElementById('forward_tr'+pk).value = ''
        document.getElementById('backward_tr'+pk).value = ''
        document.getElementById('return_tr'+pk).value = ''
    } else {
        document.getElementById("forward_tr"+pk).readOnly = true;
    }
}

function editTrReturn(pk) {
    var fac_ndd = document.getElementById("fac_ndd"+pk);
    if (fac_ndd.options[fac_ndd.selectedIndex].value == '1') {
        document.getElementById("return_tr"+pk).readOnly = false;
        document.getElementById('return_tr'+pk).value = ''
    } else {
        document.getElementById("return_tr"+pk).readOnly = true;
    }
}

// Selected customer to show shipper choices
function submitPrincipal(value){
    var principal=document.getElementById("principal_selected");
    principal.value = value;

    document.getElementById("addForm").submit();
}