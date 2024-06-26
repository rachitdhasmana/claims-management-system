$(document).ready(function() {
$('#login-form').submit(function(event) {
    event.preventDefault();
    var username = $('#username').val();
    var password = $('#password').val();
    $.ajax({
        url: '/login',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({username: username, password: password}),
        success: function(response) {
            localStorage.setItem('token', response.access_token);
            window.location.href = '/claims';
        },
        error: function(response) {
            alert('Login failed');
            window.location.href = '/';
        }
    });
});
});