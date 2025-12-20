# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend templates
COPY backend/ backend/
COPY frontend/templates/ frontend/templates/

# Copy data folder
COPY data/ data/

# Expose Flask port
EXPOSE 5002

# Run the app
CMD ["python", "backend/app.py"]
