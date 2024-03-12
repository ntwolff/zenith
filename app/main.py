import faust
from fastapi import FastAPI
from app.api.router import router as api_router
from app.processors.customer_event_graph_processor import CustomerEventGraphProcessor
from app.models.event import CustomerEvent
from .graph.database import Neo4jGraphDatabase
from datetime import timedelta, datetime

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

@app.agent(customer_event_topic)
async def process_customer_event(events):
    async for event in events:
        processor = CustomerEventGraphProcessor(graph_database)
        processor.process(event)


# ------------------------------------------------
# @TODO Refactor code below into app/processors/
# ------------------------------------------------

# Ip Address

## Windowed aggregation
ip_velocity_table = app.Table('ip_velocity', default=int, partitions=8).tumbling(
    size=timedelta(minutes=5),
    expires=timedelta(hours=1),
)

@app.agent(customer_event_topic)
async def detect_high_velocity_ip_usage(stream):
    async for event in stream.group_by(CustomerEvent.ip_address.id):
        ip_velocity_table[event.ip_address.id] += 1
        if ip_velocity_table[event.ip_address.id].now() > 1:
            print(f"Detected {ip_velocity_table[event.ip_address.id].now()} in the past 5 minutes for ip address: {event.ip_address.id}")
            await risky_ip_topic.send(value=event.ip_address.id)

@app.agent(risky_ip_topic)
async def process_high_velocity_ip(stream):
    async for ip in stream:        
        # Update the IpAddress node in the graph database
        query = """
            MATCH (i:IpAddress {id: $ip})
            SET i.risky = True, i.risky_since = datetime(), i.risky_reason = "High Velocity IP"
        """
        graph_database.execute_query(query, ip=ip)

        print(f"Processed high velocity logins to graph: {ip}")

        # query = """
            # MATCH (i:IpAddress {risky: True})<-[:USED]-(c:Customer)
            # MATCH (c)-[:PERFORMS]->(e:Event)-[:HAS]->(i)
            # RETURN i, c, count(e)
            # RETURN i.ipv4, c.id, c.first_name, c.last_name, c.email, count(e)
        # """
        # results = graph_database.execute_query(query)


# Customer Login Events

## Windowed aggregation
login_velocity_table = app.Table('login_velocity', default=int, partitions=8).tumbling(
    size=timedelta(minutes=5),
    expires=timedelta(hours=1),
)

@app.agent(customer_event_topic)
async def detect_high_velocity_customer_login(stream):
    async for event in stream.filter(lambda e: e.type == "login").group_by(CustomerEvent.customer.id):
        login_velocity_table[event.customer.id] += 1
        if login_velocity_table[event.customer.id].now() > 1:
            print(f"Detected {login_velocity_table[event.customer.id].now()} logins in the past 5 minutes for customer id: {event.customer.id}")
            await risky_logins_topic.send(value=event.customer.id)

@app.agent(risky_logins_topic)
async def process_high_velocity_logins(stream):
    async for customer_id in stream:        
        # Update the Customer node in the graph database
        query = """
            MATCH (c:Customer {id: $customer_id})
            SET c.risky = True, c.risky_since = datetime(), c.risky_reason = "High Velocity Logins"
        """
        graph_database.execute_query(query, customer_id=customer_id)

        print(f"Processed high velocity logins to graph: {customer_id}")