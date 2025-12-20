FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend
COPY frontend frontend

# Ensure data folder exists
RUN mkdir -p /app/data

EXPOSE 5002

CMD ["python", "backend/app.py"]
