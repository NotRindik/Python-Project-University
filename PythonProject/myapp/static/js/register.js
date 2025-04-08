
    document.querySelector('.helptext').style.display = 'none';
    document.querySelector('ul').style.display = 'none';

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
                alert("Форма отправлена!");
                            form.submit();
        }
    });
});
