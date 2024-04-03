# Zenith: Graph-Backed Streaming Fraud Detection 

Welcome to Zenith, a state-of-the-art analytical data streaming solution that is built atop Faust, Kafka, Neo4j, FastAPI, and more.

## 📚 Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Local Development](#local-development)
- [Additional Resources](#additional-resources)

## 🚀 Getting Started

To get Zenith up and running:

1. **Clone the repo**: [Github Link](http://github.com/ntwolff/zenith)
2. **Set-up your `.env` file**: Copy `.env.example` and edit as needed.

### Docker

1. **Start the services:**
    ```sh
    docker-compose up -d
    ```

2. **Check the logs:**
    ```sh
    docker-compose logs -f
    ```

3. **Stop the services:**
    ```sh
    docker-compose down
    ```

4. **Clean the local Docker environment (Nuclear Option):**
    ```sh
    docker system prune -a --volumes
    ```

## 🖥️ Usage

Once its running, here are ways you can interact with it:

- **Kafka Dashboard:** Access the dashboard at [`http://localhost:3030`](http://localhost:3030).
- **FastAPI OpenAPI Docs:** Explore the API at [`http://localhost:8000/docs`](http://localhost:8000/docs).
- **Neo4j Graph Viz:** Download *Neo4j Desktop* and create a new project with a *Remote DBMS*. Use the connection string `neo4j://localhost:7687` and open *Neo4j Browser* to visualize the graph.

## 💻 Local Development

For local development, follow these steps:

- **Install requirements:** Run `pip install .` (utilizes setup.py).
- **Linting:** Run `pylint $(git ls-files '*.py')`.
- **Testing:** Run `pytest tests/`.

## 📚 Additional Resources

- [Project @TODO List](docs/TODO.md)
