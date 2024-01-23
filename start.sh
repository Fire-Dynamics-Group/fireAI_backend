#!/bin/bash

# Echo the port number
echo "Starting application on port: ${PORT:-8000}"

# Start the Uvicorn server
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
