# Gunakan Python image resmi
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Salin file
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Port yang digunakan Google Cloud Run
ENV PORT 8080

# Jalankan Flask app dengan gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
