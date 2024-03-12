import faust
from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.processors.customer_event_graph_processor import CustomerEventGraphProcessor
from app.models.event import CustomerEvent
from .graph.database import Neo4jGraphDatabase
from datetime import timedelta, datetime

app = faust.App('fraud-detection-system', broker='kafka://kafka:9092')

# Neo4j
graph_database = Neo4jGraphDatabase()

customer_event_topic = app.topic('customer_event', value_type=CustomerEvent)
high_velocity_topic = app.topic('high_velocity_ip', value_type=str)


@app.agent(customer_event_topic)
async def process_customer_event(events):
    async for event in events:
        processor = CustomerEventGraphProcessor(graph_database)
        processor.process(event)

@app.agent(customer_event_topic)
async def detect_high_velocity(stream):
    return # @TODO
    async for event in stream.group_by(CustomerEvent.ip_address):
        # @TODO Move to velocity processor
        # processor = CustomerEventVelocityProcessor(graph_database)
        # processor.process(event)

        events_per_ip = stream.events()        
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        date_object = datetime.strptime(event.timestamp, date_format)

        one_min_ago = date_object - timedelta(minutes=1)
        
        recent_events = [e async for e in events_per_ip if e.timestamp & e.timestamp >= one_min_ago]
        
        if len(recent_events) > 10:
            await high_velocity_topic.send(value=event.ip_address.id)

@app.agent(high_velocity_topic)
async def process_high_velocity_ip(ips):
    return # @TODO
    async for ip in ips:
        # @TODO Move to high velocity processor
        # processor = CustomerEventHighVelocityProcessor(graph_database)
        # processor.process(event)

        print(f"High velocity IP detected: {ip}")
        
        # Update the IpAddress node in the graph database
        query = """
            MATCH (i:IpAddress {id: $ip})
            SET i.high_velocity = True
        """
        graph_database.execute_query(query, ip=ip)



# FastAPI
fastapi_app = FastAPI()
fastapi_app.include_router(api_router, prefix="/api", tags=["api"])