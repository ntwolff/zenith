FROM python:3.8

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./wait-for-kafka.sh", "kafka", "faust", "-A", "app.main", "worker", "-l", "info"]
#CMD ["uvicorn", "app.main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]