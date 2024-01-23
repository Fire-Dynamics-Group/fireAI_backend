# Echo the port number for debugging
echo "Port variable is set to: '${PORT}'"

# Check if PORT is not set or empty
if [ -z "$PORT" ]; then
    echo "WARNING: \$PORT variable is not set. Defaulting to 8000."
    PORT=8000
fi

# Start the Uvicorn server
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT