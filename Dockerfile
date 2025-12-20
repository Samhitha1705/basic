FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (to leverage caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend backend

# Copy frontend templates correctly
COPY frontend/templates templates

EXPOSE 5002

CMD ["python", "backend/app.py"]
