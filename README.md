# README.md
# Zenith Fraud Detection System

The Zenith Fraud Detection System is a proof-of-concept application that demonstrates real-time fraud detection using Kafka, Faust, Neo4j, and FastAPI.

## Features

- Process customer registration and login events in real-time
- Store and analyze customer and event data in a graph database (Neo4j)
- Expose API endpoints for handling events

## Installation

1. Clone the repository:
```sh
git clone https://github.com/ntwolff/zenith-fraud-detection.git
cd fraud-detection
```

2. Start the services using Docker Compose:
```sh
docker-compose up -d
```

To rebuild the Docker images:
```sh
# docker-compose up --scale fake-data-producer=3
docker-compose build
```

To see the Docker logs:
```sh
docker-compose logs -f
```

## Usage

- Send customer registration events to the Kafka topic `customer_registration`.
- Send login events to the Kafka topic `login`.
- Access the API endpoints:
- POST `/events/customer-registration`: Handle a customer registration event.
- POST `/events/login`: Handle a login event.