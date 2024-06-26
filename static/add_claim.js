function addClaim() {
    var token = localStorage.getItem('token');
    console.log(token);
    if (!token) {
        window.location.href = '/login';
    }

    const form = document.getElementById('claimForm');
    const formData = new FormData(form);
    formData.append('title', document.getElementById('title').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('type', document.getElementById('type').value);
    formData.append('value', document.getElementById('value').value);

    $.ajax({
        url: '/api/claims',
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        processData: false,
        contentType: false,
        cache: false,
        data: formData,
        success: function(response) {
            alert('Claim added successfully');
            window.location.href = '/claims';
        },
        error: function(response) {
            alert('Claim addition failed');
        }
    });

}
