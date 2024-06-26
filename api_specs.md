
---

# Claims Management API

## Overview

The Claims Management API provides endpoints for user registration, authentication, and CRUD operations on claims. This document outlines the available endpoints, their request parameters, response formats, and authentication mechanisms.

## Base URL

```
http://localhost:5000
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Obtain the token by logging in and include it in the `Authorization` header as a Bearer token for protected endpoints.

## Endpoints

### User Registration

#### POST /register

Registers a new user.

**Request:**

- **Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "role": "string" // "admin" or "user"
  }
  ```

**Responses:**

- **201 Created:**
  ```json
  {
    "message": "User registered successfully"
  }
  ```
- **400 Bad Request:**
  ```json
  {
    "error": "Invalid input"
  }
  ```

### User Login

#### POST /login

Logs in a user and returns a JWT token.

**Request:**

- **Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

**Responses:**

- **200 OK:**
  ```json
  {
    "access_token": "string"
  }
  ```
- **401 Unauthorized:**
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

### Create Claim

#### POST /api/claims

Creates a new claim. Requires authentication.

**Request:**

- **Headers:**
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

- **Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "string", // "type 1", "type 2", or "type 3"
    "value": "number",
    "attachment": "string"
  }
  ```

**Responses:**

- **201 Created:**
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "title": "string",
    "description": "string",
    "type": "string",
    "value": "number",
    "status": "string", // "new"
    "attachment": "string"
  }
  ```
- **400 Bad Request:**
  ```json
  {
    "error": "Invalid input"
  }
  ```
- **401 Unauthorized:**
  ```json
  {
    "error": "Unauthorized"
  }
  ```

### Get All Claims

#### GET /api/claims

Fetches all claims. Requires authentication. Admins see all claims, users see only their own claims.

**Request:**

- **Headers:**
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

**Responses:**

- **200 OK:**
  ```json
  [
    {
      "id": "integer",
      "user_id": "integer",
      "title": "string",
      "description": "string",
      "type": "string",
      "value": "number",
      "status": "string",
      "attachment": "string"
    }
  ]
  ```
- **401 Unauthorized:**
  ```json
  {
    "error": "Unauthorized"
  }
  ```

### Update Claim

#### PUT /api/claims/{claim_id}

Updates a claim. Requires authentication. Users can only update their own claims.

**Request:**

- **Headers:**
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

- **Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "string",
    "value": "number",
    "attachment": "string"
  }
  ```

**Responses:**

- **200 OK:**
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "title": "string",
    "description": "string",
    "type": "string",
    "value": "number",
    "status": "string",
    "attachment": "string"
  }
  ```
- **400 Bad Request:**
  ```json
  {
    "error": "Invalid input"
  }
  ```
- **401 Unauthorized:**
  ```json
  {
    "error": "Unauthorized"
  }
  ```
- **403 Forbidden:**
  ```json
  {
    "error": "Forbidden"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Claim not found"
  }
  ```

### Delete Claim

#### DELETE /api/claims/{claim_id}

Deletes a claim. Requires authentication. Admins can delete any claim, users can only delete their own claims.

**Request:**

- **Headers:**
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

**Responses:**

- **200 OK:**
  ```json
  {
    "message": "Claim deleted"
  }
  ```
- **401 Unauthorized:**
  ```json
  {
    "error": "Unauthorized"
  }
  ```
- **403 Forbidden:**
  ```json
  {
    "error": "Forbidden"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Claim not found"
  }
  ```

## Models

### User

- **UserRegister:**
  ```json
  {
    "username": "string",
    "password": "string",
    "role": "string" // "admin" or "user"
  }
  ```

- **UserLogin:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Claim

- **Claim:**
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "title": "string",
    "description": "string",
    "type": "string",
    "value": "number",
    "status": "string",
    "attachment": "string"
  }
  ```

- **CreateClaim:**
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "string", // "type 1", "type 2", or "type 3"
    "value": "number",
    "attachment": "string"
  }
  ```

- **UpdateClaim:**
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "string",
    "value": "number",
    "status": "string", // "new", "acknowledged", "approved", "denied"
    "attachment": "string"
  }
  ```

### Responses

- **MessageResponse:**
  ```json
  {
    "message": "string"
  }
  ```

- **ErrorResponse:**
  ```json
  {
    "error": "string"
  }
  ```

- **LoginResponse:**
  ```json
  {
    "access_token": "string"
  }
  ```

---


## Summary

This document provides a comprehensive specification for the Claims Management API, detailing each endpoint's request and response formats, including models and authentication requirements. This will help developers understand how to interact with the API and what to expect in terms of data and security.
This API allows you to manage claims with the following operations:

1. **Get All Claims {role: user}**: Retrieve a list of all claims created by user.
2. **Get All Claims {role: admin}**: Retrieve a list of all claims created by all users.
2. **Create a New Claim**: Add a new claim with a title, description, type, value, and optional attachment.
3. **Update an Existing Claim**: Modify the details of an existing claim, including its status.
4. **Delete an Existing Claim**: Remove a claim by its ID.

Each claim includes the following fields:

- **id**: Unique identifier for the claim.
- **user-id**: Unique identifier of the user/owner of the claim.
- **title**: Title of the claim.
- **description**: Description of the claim.
- **type**: Type of the claim (e.g., type 1, type 2, type 3).
- **value**: Monetary value of the claim.
- **status**: Current status of the claim (e.g., new, acknowledged, approved, denied).
- **attachment**: Filename of the attached document (if any).
