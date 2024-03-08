# Zenith Event Intelligence
This is a poc fraud detection system that processes customer events in real-time using Kafka, Faust, Neo4j, RocksDB, and FastAPI.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:
```sh
git clone https://github.com/your-repo/fraud-detection.git
cd fraud-detection
```

2. Start the services using Docker Compose:
```sh
docker-compose up -d
```

3. Install the Python dependencies:
```sh
pip install -r requirements.txt
```

4. Run the Faust application:
```sh
faust -A app.main worker -l info
```

5. Run the FastAPI server:
```sh
uvicorn api.endpoints:app --reload
```

The fraud detection system should now be up and running. You can send customer events to the Kafka topic and the system will process them in real-time, updating the Neo4j graph and RocksDB accordingly. The FastAPI server exposes an endpoint to retrieve customer data along with the associated fraud vectors.

## Local Test Data
Faust agents in `/tests/fakes` will produce local test data.

```sh
faust -A tests.fakes.customer_event_producer worker -l info
```

## Structure

```
event-intelligence/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agents.py
│   └── graph.py
│
├── api/
│   ├── __init__.py
│   └── endpoints.py
│
├── README.md
├── requirements.txt
└── docker-compose.yml
```