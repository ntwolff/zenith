from fastapi import APIRouter
from ..events.models import CustomerRegistrationEvent, LoginEvent
from ..events.processors import CustomerRegistrationEventProcessor, LoginEventProcessor
from ..graph.database import Neo4jGraphDatabase

router = APIRouter()

@router.post("/events/customer-registration")
def handle_customer_registration_event(event: CustomerRegistrationEvent):
    graph_database = Neo4jGraphDatabase("bolt://localhost:7687", ("neo4j", "password"))
    processor = CustomerRegistrationEventProcessor(graph_database)
    processor.process(event)

@router.post("/events/login")
def handle_login_event(event: LoginEvent):
    graph_database = Neo4jGraphDatabase("bolt://localhost:7687", ("neo4j", "password"))
    processor = LoginEventProcessor(graph_database)
    processor.process(event)