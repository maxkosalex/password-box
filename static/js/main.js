
const input_name = document.getElementById('input_name');
const input_email = document.getElementById('input_email');
const input_password = document.getElementById('input_password');
const additional_btn = document.getElementById('additional_btn');



function checkinputs(){
    if (input_name.value && input_email.value && input_password.value) {
        additional_btn.removeAttribute('disabled');

    }
    else {
        additional_btn.setAttribute('disabled', true);

  }

}

var name = document.getElementById("input_name").value;
var email = document.getElementById("input_email").value;
var password = document.getElementById("input_password").value;

function input_data(){
    name = document.getElementById("input_name").value;
    email = document.getElementById("input_email").value;
    password = document.getElementById("input_password").value;

}

input_name.addEventListener('input', checkinputs);
input_email.addEventListener('input', checkinputs);
input_password.addEventListener('input', checkinputs);

function popup_open() {
    document.getElementById('popup').classList.add('open');
    clear_inputs();

}

function popup_add() {
    document.getElementById('popup').classList.remove('open');
    additional_btn.setAttribute('disabled', true);
    clear_inputs();

}

function popup_close() {
    document.getElementById('popup').classList.remove('open');
    additional_btn.setAttribute('disabled', true);
    clear_inputs();
}

function clear_inputs(){
    var inputElements = document.querySelectorAll('input');

    for (var i=0; i < inputElements.length; i++) {
        if (inputElements[i].type == 'text') {
        inputElements[i].value = '';

        }

    }

}
