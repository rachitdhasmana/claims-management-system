## Claims Management System

This project is a simple full-stack application for managing claims. It uses Python Flask as the backend and HTML/JavaScript for the frontend. The application supports creating, reading, updating, and deleting claims, with additional support for claim types, statuses, and file attachments.

### Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Running with Docker](#running-with-docker)
6. [API Endpoints](#api-endpoints)
7. [Running Tests](#running-tests)
8. [Folder Structure](#folder-structure)

### Features

- Add, view, update, and delete claims.
- Claims have titles, descriptions, types, values, statuses, and attachments.
- Supports file uploads for attachments.
- Claims statuses can be changed and include: new, acknowledged, approved, and denied.

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Flask
- Flask-SQLAlchemy

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/rachitdhasmana/claims-management-system.git
    cd claims-management-system
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Run the Flask application**:
    ```sh
    flask run
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000` to see the application.


### Running with Docker

1. Build the Docker image:
    ```sh
    docker build -t claims-management-system .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 5050:5050 -p 8080:8080 claims-management-system
    ```

3. Open your browser and navigate to `http://localhost:5050` to view the application.

   The uploaded files can be accessed via `http://localhost:8080`.


### API Endpoints

- **GET /api/claims**
    - Fetch all claims.
    - Response: JSON array of claims.
  
- **POST /api/claims**
    - Create a new claim.
    - Request: Form data including title, description, claim_type, claim_value, and optional attachment file.
    - Response: JSON object of the created claim.

- **PUT /api/claims/<id>**
    - Update an existing claim by ID.
    - Request: JSON object including title, description, claim_type, claim_value, and status.
    - Response: JSON object of the updated claim.

- **DELETE /api/claims/<id>**
    - Delete an existing claim by ID.
    - Response: JSON message confirming deletion.

### Detailed API Specs
- **Detailed API specs can be found : [here](api_specs.md)**

### Running Tests

1. **Create a temporary file for testing purposes**:
    ```sh
    echo 'Test file content' > test_file.txt
    ```

2. **Run the tests**:
    ```sh
    python -m unittest test_app.py
    ```

3. **Clean up the temporary file**:
    ```sh
    rm test_file.txt
    ```

### Folder Structure

```
claims-management-system/
│
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Dockerfile to create Docker image
├── start.sh             # Script to start Flask app and HTTP server
├── test_app.py          # Unit tests
│
├── templates/
│   ├── index.html       # Homepage template
│   └── claims.html      # Claims listing template
│
├── static/
│   ├── index.js         # JavaScript for homepage
│   └── claims.js        # JavaScript for claims page
│
└── uploads/             # Folder for uploaded files
```

### Detailed Explanation

#### `app.py`

- **Models**: Defines the `Claim` model with fields for `title`, `description`, `claim_type`, `claim_value`, `status`, and `attachment`.
- **Routes**:
  - `/` and `/claims`: Render the main pages.
  - `/api/claims`: API endpoints for managing claims.
  - Handles file uploads for claim attachments.

#### `templates/index.html`

- Form for adding new claims with fields for title, description, type, value, and file upload.
- Links to the claims listing page.

#### `templates/claims.html`

- Displays all claims with options to update or delete each one.
- Includes fields for title, description, type, value, status, and attachment.

#### `static/index.js`

- Handles adding new claims via the form on the homepage.

#### `static/claims.js`

- Fetches and displays all claims.
- Handles updating and deleting claims.

#### `test_app.py`

- Unit tests for the application covering adding, retrieving, updating, and deleting claims.

### Conclusion

This project provides a complete full-stack solution for managing claims with support for various claim types, statuses, and file attachments. The detailed instructions above should help you set up, run, and test the application efficiently. Feel free to contribute and improve the project by opening issues or pull requests on GitHub.