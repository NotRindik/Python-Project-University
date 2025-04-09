
document.querySelector('.helptext').style.display = 'none';
document.querySelector('ul').style.display = 'none';

const password_help_text = document.querySelector('#id_password2_helptext');
const br_el = document.createElement('br');

const parent = password_help_text.parentNode;

parent.insertBefore(br_el, password_help_text.previousSibling);

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        var passwordField = document.querySelector('[name="password1"]');
        if (passwordField && passwordField.value.length < 8) {
            document.querySelector('.helptext').style.display = 'block';
            document.querySelector('ul').style.display = 'block';
             event.preventDefault();
        }
        else{
                form.submit();
        }
    });
});
