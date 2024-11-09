# Dockerfile for containerizing backend (Python + FastAPI)
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire backend code to the container
COPY . /app

# Set PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
