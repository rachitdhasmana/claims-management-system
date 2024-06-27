$(document).ready(function() {

    localStorage.removeItem('token');
    $('#register-form').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var role = $('#role').val();
        $.ajax({
            url: '/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username, password: password, role: role}),
            success: function(response) {
                alert('User registered successfully');
                window.location.href = '/login';
            },
            error: function(response) {
                alert('Registration failed');
            }
        });
    });
});