# zenith/
# │
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── events/
# │   │   ├── __init__.py
# │   │   ├── models.py
# │   │   └── processors.py
# │   ├── graph/
# │   │   ├── __init__.py
# │   │   └── database.py
# │   └── api/
# │       ├── __init__.py
# │       └── endpoints.py
# │
# ├── tests/
# │   ├── __init__.py
# │   ├── test_events.py
# │   ├── test_graph.py
# │   └── test_api.py
# │
# ├── docs/
# │   ├── index.md
# │   ├── events.md
# │   ├── graph.md
# │   └── api.md
# │
# ├── requirements.txt
# ├── Dockerfile
# ├── docker-compose.yml
# └── README.md



"""
Zenith Fraud Detection System
==============================

This module implements a proof-of-concept fraud detection system using Kafka, Faust, Neo4j, and FastAPI.
The system follows the SOLID principles for a modular, extensible, and maintainable codebase.

The main components of the system are:
- Event models: Define the structure of different event types.
- Event processors: Handle the processing of events and perform necessary actions.
- Graph database: Interacts with the Neo4j graph database for storing and retrieving data.
- API endpoints: Expose the functionality of the system through a RESTful API.

The system is designed to be easily extensible, allowing the addition of new event types and processors
without modifying the existing code.

Author: Your Name
"""

from abc import ABC, abstractmethod
from typing import List

import faust
from fastapi import FastAPI
from neo4j import GraphDatabase

app = faust.App('zenith-fraud-detection', broker='kafka://localhost:9092')
fastapi_app = FastAPI()


