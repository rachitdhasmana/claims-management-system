function addClaim() {
    const form = document.getElementById('claimForm');
    const formData = new FormData(form);
    formData.append('title', document.getElementById('title').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('claim_type', document.getElementById('claim_type').value);
    formData.append('claim_value', document.getElementById('claim_value').value);

    fetch('/api/claims', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = 'Claim added successfully!';
        document.getElementById('title').value = '';
        document.getElementById('description').value = '';
        document.getElementById('claim_type').value = 'type 1';
        document.getElementById('claim_value').value = '';
        document.getElementById('attachment').value = '';
    })
    .catch(error => console.error('Error adding claim:', error));
}
