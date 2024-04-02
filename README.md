# Zenith - Streaming Fraud Detection System

Zenith is a proof-of-concept application that is intended to demonstrate real-time fraud detection, integrated to a graph database, using a tech stack that includes:
- Kafka
- Faust (faust-streaming)
- Neo4j
- FastAPI

Zenith is focused on consumer lending use cases, with a goal of creating a system that serves as both a real-time decisioning mechanism on transactions, and a tool to empower fraud specialists in their investigations.  The expected applications are across all relevant fraud use cases (e.g. account takeover, application fraud, credit card transaction fraud), and beyond fraud as a general purpose mechanism.

## Features

- Process and act on events in real-time.
- Perform powerful graph analytics.
- User-friendly API for administrative and operational use-cases.

## Installation

1. Clone the repository:
```sh
git clone https://github.com/ntwolff/zenith.git
cd zenith
```

2. Rename `.env.example` to `.env` and update dummy values:

3. Build and start the services using Docker Compose:
```sh
docker-compose up --build -d
```

To see the Docker logs:
```sh
docker-compose logs -f
```

To stop the services:
```sh
docker-compose down
```

To *fully* clean the local docker environment [nuclear option]:
```sh
docker system prune -a --volumes
```

## Usage

- Kafka Management: `http://localhost:3030`
- OpenAPI Documentation: `http://localhost:8000/docs`
- Neo4j Visualization:
    - Download **Neo4j Desktop**
    - Create a new project with a *Remote DBMS*.  Connection string: `neo4j://localhost:7687`
    - Open the Neo4j browser to visualize the graph.
- Local Development:
    - Installing reqs: `pip install .` (utilizes setup.py)
    - Linting: `pylint $(git ls-files '*.py')`
    - Testing: `pytest tests/`