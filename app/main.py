# app/main.py
from app.config.settings import settings
import faust
from fastapi import FastAPI
from app.api.router import router as api_router
from app.processors import CustomerEventGraphProcessor, HighVelocityIpProcessor, HighVelocityLoginProcessor, HighVelocityEventProcessor
from app.models import CustomerEvent, HighVelocityEvent
from app.database.neo4j_database import Neo4jDatabase
from datetime import timedelta

# Kafka / Faust
app = faust.App(settings.faust_app_name, broker=settings.faust_broker)
customer_event_topic = app.topic('customer_event', value_type=CustomerEvent, partitions=settings.kafka_topic_partitions)
high_velocity_topic = app.topic('high_velocity_event', value_type=HighVelocityEvent)

# Neo4j
graph_database = Neo4jDatabase(
    uri=settings.neo4j_uri,
    user=settings.neo4j_user,
    password=settings.neo4j_password
)

# FastAPI
fastapi_app = FastAPI()
fastapi_app.include_router(api_router, prefix="/api")

@app.agent(customer_event_topic)
async def process_customer_event(events):
    async for event in events:
        processor = CustomerEventGraphProcessor(graph_database)
        processor.process(event)

# High Velocity IP Processor
high_velocity_ip_processor = HighVelocityIpProcessor(
    app,
    window_size=timedelta(minutes=settings.high_velocity_ip_window_size),
    window_expires=timedelta(minutes=settings.high_velocity_ip_window_expires)
)

@app.agent(customer_event_topic)
async def detect_high_velocity_ip_usage(stream):
    await high_velocity_ip_processor.detect_high_velocity_ip_usage(stream)

# High Velocity Login Processor
high_velocity_login_processor = HighVelocityLoginProcessor(
    app, 
    window_size=timedelta(minutes=settings.high_velocity_login_window_size),
    window_expires=timedelta(minutes=settings.high_velocity_login_window_expires)
)

@app.agent(customer_event_topic)
async def detect_high_velocity_customer_login(stream):
    await high_velocity_login_processor.detect_high_velocity_customer_login(stream)

# High Velocity Event Processor
high_velocity_event_processor = HighVelocityEventProcessor(app, graph_database)

@app.agent(high_velocity_topic)
async def process_high_velocity_event(stream):
    await high_velocity_event_processor.process_high_velocity_event(stream)


@fastapi_app.on_event("shutdown")
def shutdown_event():
    graph_database.close()