# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and templates
COPY backend backend
COPY frontend/templates templates

# Expose the port your Flask app uses
EXPOSE 5002

# Start the Flask app
CMD ["python", "backend/app.py"]
