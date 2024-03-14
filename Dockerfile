FROM python:3.8

RUN apt-get update && apt-get install -y netcat-openbsd curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./wait-for-neo4j.sh", "neo4j", "./wait-for-kafka.sh", "fast-data-dev", "faust", "-A", "app.main", "worker", "-l", "info"]