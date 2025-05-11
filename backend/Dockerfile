FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /var/log/apache2 && chmod -R 755 /var/log/apache2

COPY . .

EXPOSE 5000


CMD ["gunicorn","-k","eventlet","-w","1","-b","0.0.0.0:8000","run:app"]
