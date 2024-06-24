document.addEventListener('DOMContentLoaded', fetchClaims);

function fetchClaims() {
    fetch('/api/claims')
        .then(response => response.json())
        .then(data => {
            const claimsDiv = document.getElementById('claims');
            claimsDiv.innerHTML = '';
            data.forEach(claim => {
                const claimDiv = document.createElement('div');
                claimDiv.className = 'claim';
                claimDiv.innerHTML = `
                    <input type="text" value="${claim.title}" data-id="${claim.id}" class="title">
                    <input type="text" value="${claim.description}" data-id="${claim.id}" class="description">
                    <select data-id="${claim.id}" class="claim_type">
                        <option value="type 1" ${claim.claim_type === 'type 1' ? 'selected' : ''}>Type 1</option>
                        <option value="type 2" ${claim.claim_type === 'type 2' ? 'selected' : ''}>Type 2</option>
                        <option value="type 3" ${claim.claim_type === 'type 3' ? 'selected' : ''}>Type 3</option>
                    </select>
                    <input type="number" value="${claim.claim_value}" data-id="${claim.id}" class="claim_value">
                    <select data-id="${claim.id}" class="status">
                        <option value="new" ${claim.status === 'new' ? 'selected' : ''}>New</option>
                        <option value="acknowledged" ${claim.status === 'acknowledged' ? 'selected' : ''}>Acknowledged</option>
                        <option value="approved" ${claim.status === 'approved' ? 'selected' : ''}>Approved</option>
                        <option value="denied" ${claim.status === 'denied' ? 'selected' : ''}>Denied</option>
                    </select>
                    ${claim.attachment ? `<a href="http://localhost:8080/uploads/${claim.attachment}" target="_blank">View Attachment</a>` : ''}
                    <button onclick="updateClaim(${claim.id})">Update</button>
                    <button onclick="deleteClaim(${claim.id})">Delete</button>
                `;
                claimsDiv.appendChild(claimDiv);
            });
        })
        .catch(error => console.error('Error fetching claims:', error));
}

function updateClaim(id) {
    const title = document.querySelector(`.title[data-id='${id}']`).value;
    const description = document.querySelector(`.description[data-id='${id}']`).value;
    const claimType = document.querySelector(`.claim_type[data-id='${id}']`).value;
    const claimValue = parseFloat(document.querySelector(`.claim_value[data-id='${id}']`).value);
    const status = document.querySelector(`.status[data-id='${id}']`).value;

    fetch(`/api/claims/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, claim_type: claimType, claim_value: claimValue, status: status })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = 'Claim updated successfully!';
        fetchClaims();
    })
    .catch(error => console.error('Error updating claim:', error));
}

function deleteClaim(id) {
    fetch(`/api/claims/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = 'Claim deleted successfully!';
        fetchClaims();
    })
    .catch(error => console.error('Error deleting claim:', error));
}
