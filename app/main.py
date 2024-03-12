import faust
from fastapi import FastAPI
from app.api.router import router as api_router
from app.processors.customer_event_graph_processor import CustomerEventGraphProcessor
from app.processors.high_velocity_ip_processor import HighVelocityIpProcessor
from app.processors.high_velocity_login_processor import HighVelocityLoginProcessor
from app.models.event import CustomerEvent
from .graph.database import Neo4jGraphDatabase
from app.services.ip_address_service import IpAddressService
from app.services.customer_service import CustomerService

# Kafka / Faust
app = faust.App('fraud-detection-system', broker='kafka://kafka:9092')
customer_event_topic = app.topic('customer_event', value_type=CustomerEvent, partitions=8)
risky_ip_topic = app.topic('risky_ip', value_type=str)
risky_logins_topic = app.topic('risky_logins', value_type=str)

# Neo4j
graph_database = Neo4jGraphDatabase()

# FastAPI
fastapi_app = FastAPI()
fastapi_app.include_router(api_router, prefix="/api")

# Services
ip_address_service = IpAddressService(graph_database)
customer_service = CustomerService(graph_database)

# Customer Event Graph Processor
@app.agent(customer_event_topic)
async def process_customer_event(events):
    async for event in events:
        processor = CustomerEventGraphProcessor(graph_database)
        processor.process(event)

# High Velocity IP Processor
high_velocity_ip_processor = HighVelocityIpProcessor(app, ip_address_service)

@app.agent(customer_event_topic)
async def detect_high_velocity_ip_usage(stream):
    await high_velocity_ip_processor.detect_high_velocity_ip_usage(stream)

# High Velocity Login Processor
high_velocity_login_processor = HighVelocityLoginProcessor(app, customer_service)

@app.agent(customer_event_topic)
async def detect_high_velocity_customer_login(stream):
    await high_velocity_login_processor.detect_high_velocity_customer_login(stream)