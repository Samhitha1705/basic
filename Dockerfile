# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend templates
COPY backend backend
COPY frontend/templates templates

# Expose Flask port
EXPOSE 5002

# Start Flask app
CMD ["python", "backend/app.py"]
