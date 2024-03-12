# This file contains the FastAPI endpoints to: 
#    - Push ad-hoc events onto the stream (/events/), 
#    - Retrieve near real-time analytics endpoints to detect fraud (/fraud/).

from fastapi import APIRouter
from app.api.models import CustomerEventModel
from app.models import CustomerEvent, Customer, Address, Device, IpAddress
from app.processors import CustomerEventGraphProcessor
from app.graph.database import Neo4jGraphDatabase

router = APIRouter()

@router.post("/events/customer-event")
def handle_customer_event(event: CustomerEventModel):
    print(f"Received event: {event}")

    faust_event = CustomerEvent(
        id=event.id,
        type=event.type,
        timestamp=event.timestamp,
        customer=Customer(
            id=event.customer.id,
            email=event.customer.email,
            phone=event.customer.phone,
            first_name=event.customer.first_name,
            last_name=event.customer.last_name,
            date_of_birth=event.customer.date_of_birth,
            ssn=event.customer.ssn,
            address=Address(
                id=event.customer.address.id,
                street=event.customer.address.street,
                city=event.customer.address.city,
                state=event.customer.address.state,
                zip=event.customer.address.zip
            )
        ),
        device=Device(
            id=event.device.id,
            user_agent=event.device.user_agent
        ),
        ip_address=IpAddress(
            id=event.ip_address.id,
            ipv4=event.ip_address.ipv4
        ),
    )

    graph_database = Neo4jGraphDatabase()
    processor = CustomerEventGraphProcessor(graph_database)
    processor.process(faust_event)

@router.get("/fraud/shared-ip")
def detect_shared_ip(minutes: int = 60):
    query = """
        MATCH (c1:Customer)-[:USED]->(i:IpAddress)<-[:USED]-(c2:Customer)
        WHERE c1 <> c2
        AND c1.last_active_at > datetime() - duration({minutes: $minutes})
        AND c2.last_active_at > datetime() - duration({minutes: $minutes})
        RETURN c1, c2, i
    """
    graph_database = Neo4jGraphDatabase()
    results = graph_database.execute_query(query, minutes=minutes)
    # Process and return results
    return {"results": [{
        "customer1": record["c1"]["id"], 
        "customer2": record["c2"]["id"],
        "ip_address": record["i"]["id"]
    } for record in results]}

@router.get("/fraud/risk-scores")
def calculate_risk_scores():
    query = """
        CALL gds.graph.create('fraud-graph', ['Customer', 'Device', 'IpAddress'], {
            PERFORMS: {
                orientation: 'UNDIRECTED'
            },
            USED: {
                orientation: 'UNDIRECTED'    
            }
        })
        
        CALL gds.pageRank.stream('fraud-graph')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).id AS id, score
        ORDER BY score DESC
    """
    graph_database = Neo4jGraphDatabase()
    results = graph_database.execute_query(query)
    # Process and return risk scores
    return {"risk_scores": [{
        "id": record["id"],
        "score": record["score"]
    } for record in results]}