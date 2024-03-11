import faust
from fastapi import FastAPI
from app.api.endpoints import router as api_router

from .events.models import CustomerRegistrationEvent, LoginEvent
from .events.processors import CustomerRegistrationEventProcessor, LoginEventProcessor
from .graph.database import Neo4jGraphDatabase

app = faust.App('zenith-fraud-detection', broker='kafka://kafka:9092')
fastapi_app = FastAPI()
fastapi_app.include_router(api_router, prefix="/api", tags=["api"])

# Kafka Topics
customer_registration_topic = app.topic('customer_registration', value_type=CustomerRegistrationEvent)
login_topic = app.topic('login', value_type=LoginEvent)

# Graph Database
graph_database = Neo4jGraphDatabase("bolt://neo4j:7687", ("neo4j", "password"))

# Faust Agents
@app.agent(customer_registration_topic)
async def process_customer_registration_events(events):
    processor = CustomerRegistrationEventProcessor(graph_database)
    async for event in events:
        processor.process(event)
        print(f"Consumed fake customer registration event: {event}")

@app.agent(login_topic)
async def process_login_events(events):
    processor = LoginEventProcessor(graph_database)
    async for event in events:
        processor.process(event)
        print(f"Consumed fake login event: {event}")