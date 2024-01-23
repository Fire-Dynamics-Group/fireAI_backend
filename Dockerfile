# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install the requirements
RUN pip install -r requirements.txt

# Copy the entire project to the container
COPY . /app

# Debug: Print the PORT environment variable
RUN echo "Port: $PORT"

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
