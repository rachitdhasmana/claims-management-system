#!/bin/sh

# Start the Python HTTP server for the uploads directory
cd /app && python -m http.server 8080 &

# Start the Flask app
cd /app && flask run --port=5050
