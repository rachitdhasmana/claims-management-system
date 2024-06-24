//function addClaim() {
//    const title = document.getElementById('title').value;
//    const description = document.getElementById('description').value;
//    const claimType = document.getElementById('claim_type').value;
//    const claimValue = parseFloat(document.getElementById('claim_value').value);
//
//    fetch('/api/claims', {
//        method: 'POST',
//        headers: { 'Content-Type': 'application/json' },
//        body: JSON.stringify({ title, description, claim_type: claimType, claim_value: claimValue })
//    })
//    .then(response => response.json())
//    .then(data => {
//        document.getElementById('message').innerText = 'Claim added successfully!';
//        document.getElementById('title').value = '';
//        document.getElementById('description').value = '';
//        document.getElementById('claim_type').value = 'type 1';
//        document.getElementById('claim_value').value = '';
//    });
//}
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
