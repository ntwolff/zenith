# Zenith - Streaming Fraud Detection System

A proof-of-concept application that demonstrates real-time fraud detection using Kafka/Faust, Neo4j, and FastAPI.

## Features

- Process events in real-time
- Store and analyze data in a graph database (Neo4j)
- Expose API endpoints for handling events & analytics

## Installation

1. Clone the repository:
```sh
git clone https://github.com/ntwolff/zenith.git
cd fraud-detection
```

2. Build and start the services using Docker Compose:
```sh
# docker-compose up -d
docker-compose up --build
```

To see the Docker logs:
```sh
docker-compose logs -f
```

To stop the services:
```sh
docker-compose down
```

To clean the local environment:
```sh
docker system prune -a --volumes
```

## Usage

- Kafka 
    - Dashboard: `http://localhost:3030`
    - Topics: `customer-event`, `application-event`, `risk-signal`, `graph-management`
- FastAPI: `http://localhost:8000/docs`
- Tests: `pytest tests/`