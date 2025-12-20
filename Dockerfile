# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend
COPY backend/ backend/
COPY frontend/templates/ frontend/templates/

# Create data folder inside container
RUN mkdir -p /app/data

# Pre-create users.db inside container (optional, can remove if init_db() is enough)
RUN python -c "from backend.db import init_db; init_db()"

# Expose Flask port
EXPOSE 5002

# Run the app
CMD ["python", "backend/app.py"]
