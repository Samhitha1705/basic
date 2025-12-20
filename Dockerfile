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

# Ensure data folder exists inside container
RUN mkdir -p /app/data

# Optionally copy existing users.db if present (won't fail if missing)
COPY data/users.db /app/data/ 2>/dev/null || echo "No existing users.db, will be created at runtime"

# Expose Flask port
EXPOSE 5002

# Run the app
CMD ["python", "backend/app.py"]
