
$(document).ready(function() {

    var token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
    }

    fetchClaims();

    // add new claim
    $('#add').click(function() {
        window.location.href = '/add';
    });

    // Refresh claims on page load
    $('#refresh').click(function() {
        fetchClaims();
    });

    // Logout functionality
    $('#logout').click(function() {
        localStorage.removeItem('token');
        window.location.href = '/login';
    });
});

function sanitizeInput(input) {
    if (input) {
        return DOMPurify.sanitize(input);
    }
    return input;
}

// Function to fetch claims
function fetchClaims() {
    var token = localStorage.getItem('token');

    $.ajax({
        url: '/api/claims',
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        success: function(claims) {
            const claimsDiv = document.getElementById('claims');
            claimsDiv.innerHTML = '';
            claims.forEach(claim => {
                const claimDiv = document.createElement('div');
                claimDiv.className = 'claim';
                claimDiv.innerHTML = `
                    <input type="text" value="${sanitizeInput(claim.title)}" data-id="${claim.id}" class="title">
                    <input type="text" value="${sanitizeInput(claim.description)}" data-id="${claim.id}" class="description">
                    <select data-id="${claim.id}" class="type">
                        <option value="type 1" ${sanitizeInput(claim.type) === 'type 1' ? 'selected' : ''}>Type 1</option>
                        <option value="type 2" ${sanitizeInput(claim.type) === 'type 2' ? 'selected' : ''}>Type 2</option>
                        <option value="type 3" ${sanitizeInput(claim.type) === 'type 3' ? 'selected' : ''}>Type 3</option>
                    </select>
                    <input type="number" value="${sanitizeInput(claim.value)}" data-id="${claim.id}" class="value">

                    <select data-id="${claim.id}" class="status" ${claim.allow_status_edit?'':'disabled'}>
                        <option value="new" ${sanitizeInput(claim.status) === 'new' ? 'selected' : ''}>New</option>
                        <option value="acknowledged" ${sanitizeInput(claim.status) === 'acknowledged' ? 'selected' : ''}>Acknowledged</option>
                        <option value="approved" ${sanitizeInput(claim.status) === 'approved' ? 'selected' : ''}>Approved</option>
                        <option value="denied" ${sanitizeInput(claim.status) === 'denied' ? 'selected' : ''}>Denied</option>
                    </select>

                    ${claim.attachment ? `<a href="http://localhost:8080/uploads/${claim.attachment}" target="_blank">View Attachment</a>` : ''}
                    <button onclick="updateClaim(${claim.id})">Update</button>
                    <button onclick="deleteClaim(${claim.id})">Delete</button>
                `;
                claimsDiv.appendChild(claimDiv);

            });
        },
        error: function(response) {
//            alert('Failed to fetch claims');
        }
    });
}

function updateClaim(id) {
    var token = localStorage.getItem('token');

    const title = document.querySelector(`.title[data-id='${id}']`).value;
    const description = document.querySelector(`.description[data-id='${id}']`).value;
    const type = document.querySelector(`.type[data-id='${id}']`).value;
    const value = parseFloat(document.querySelector(`.value[data-id='${id}']`).value);
    const status = document.querySelector(`.status[data-id='${id}']`).value;

    $.ajax({
        url: `/api/claims/${id}`,
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        contentType: 'application/json',
        data: JSON.stringify({
            title: title,
            description: description,
            type: type,
            value: value,
            status: status
        }),

        success: function(response) {
            alert('Claim updated successfully');
            window.location.href = '/claims';
        },
        error: function(response) {
            alert('Claim inundation failed');
        }
    });
}

function deleteClaim(id) {
    var token = localStorage.getItem('token');

    $.ajax({
        url: `/api/claims/${id}`,
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        success: function(response) {
            alert('Claim deleted successfully');
            window.location.href = '/claims';
        },
        error: function(response) {
            alert('Claim deletion failed');
        }
    });

}
