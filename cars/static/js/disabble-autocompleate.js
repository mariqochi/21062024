// JavaScript to disable autocomplete for password fields

document.addEventListener("DOMContentLoaded", function() {
    var passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function(field) {
        field.setAttribute("autocomplete", "new-password");
    });
});