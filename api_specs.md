Sure! Here is a detailed API specification for the Claims Management System.

---

# Claims Management API

## Base URL

The base URL for the API is `http://127.0.0.1:5000/api`

## Endpoints

### 1. Get All Claims

**Endpoint:** `GET /claims`

Fetch all claims in the system.

**Request:**

- Method: `GET`
- URL: `/api/claims`

**Response:**

- Status Code: `200 OK`
- Body: JSON array of claims

**Response Example:**

```json
[
    {
        "id": 1,
        "title": "Test Claim",
        "description": "Test Description",
        "claim_type": "type 1",
        "claim_value": 100.0,
        "status": "new",
        "attachment": "test_file.txt"
    }
]
```

### 2. Create a New Claim

**Endpoint:** `POST /claims`

Create a new claim.

**Request:**

- Method: `POST`
- URL: `/api/claims`
- Body: Form data including `title`, `description`, `claim_type`, `claim_value`, and optional `attachment` file.

**Request Example:**

```
Content-Type: multipart/form-data

title=Test Claim&description=Test Description&claim_type=type 1&claim_value=100.0&attachment=test_file.txt
```

**Response:**

- Status Code: `200 OK`
- Body: JSON object of the created claim

**Response Example:**

```json
{
    "id": 1,
    "title": "Test Claim",
    "description": "Test Description",
    "claim_type": "type 1",
    "claim_value": 100.0,
    "status": "new",
    "attachment": "test_file.txt"
}
```

### 3. Update an Existing Claim

**Endpoint:** `PUT /claims/<id>`

Update an existing claim by ID.

**Request:**

- Method: `PUT`
- URL: `/api/claims/<id>`
- Body: JSON object including `title`, `description`, `claim_type`, `claim_value`, and `status`.

**Request Example:**

```
Content-Type: application/json

{
    "title": "Updated Title",
    "description": "Updated Description",
    "claim_type": "type 2",
    "claim_value": 200.0,
    "status": "acknowledged"
}
```

**Response:**

- Status Code: `200 OK`
- Body: JSON object of the updated claim

**Response Example:**

```json
{
    "id": 1,
    "title": "Updated Title",
    "description": "Updated Description",
    "claim_type": "type 2",
    "claim_value": 200.0,
    "status": "acknowledged",
    "attachment": "test_file.txt"
}
```

### 4. Delete an Existing Claim

**Endpoint:** `DELETE /claims/<id>`

Delete an existing claim by ID.

**Request:**

- Method: `DELETE`
- URL: `/api/claims/<id>`

**Response:**

- Status Code: `200 OK`
- Body: JSON message confirming deletion

**Response Example:**

```json
{
    "message": "Claim deleted"
}
```

---

## Summary

This API allows you to manage claims with the following operations:

1. **Get All Claims**: Retrieve a list of all claims.
2. **Create a New Claim**: Add a new claim with a title, description, type, value, and optional attachment.
3. **Update an Existing Claim**: Modify the details of an existing claim, including its status.
4. **Delete an Existing Claim**: Remove a claim by its ID.

Each claim includes the following fields:

- **id**: Unique identifier for the claim.
- **title**: Title of the claim.
- **description**: Description of the claim.
- **claim_type**: Type of the claim (e.g., type 1, type 2, type 3).
- **claim_value**: Monetary value of the claim.
- **status**: Current status of the claim (e.g., new, acknowledged, approved, denied).
- **attachment**: Filename of the attached document (if any).

Ensure you handle file uploads and JSON data appropriately when interacting with the API.