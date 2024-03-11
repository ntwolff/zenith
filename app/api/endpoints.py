from fastapi import APIRouter
from app.api.models import CustomerRegistrationEventModel, LoginEventModel
from app.events.models import CustomerRegistrationEvent, LoginEvent
from app.events.processors import CustomerRegistrationEventProcessor, LoginEventProcessor
from app.graph.database import Neo4jGraphDatabase

router = APIRouter()

@router.post("/events/customer-registration")
def handle_customer_registration_event(event: CustomerRegistrationEventModel):
    # Convert the Pydantic model to a Faust record
    faust_event = CustomerRegistrationEvent(
        customer_id=event.customer_id,
        timestamp=event.timestamp,
        email=event.email,
        phone_number=event.phone_number,
        device=event.device.dict(),
        ip_address=event.ip_address.dict()
    )

    # Process the event
    graph_database = Neo4jGraphDatabase("bolt://neo4j:7687", ("neo4j", "password"))
    processor = CustomerRegistrationEventProcessor(graph_database)
    processor.process(event)

@router.post("/events/login")
def handle_login_event(event: LoginEventModel):
    # Convert the Pydantic model to a Faust record
    faust_event = LoginEvent(
        customer_id=event.customer_id,
        timestamp=event.timestamp,
        device=event.device.dict(),
        ip_address=event.ip_address.dict()
    )

    # Process the event
    graph_database = Neo4jGraphDatabase("bolt://neo4j:7687", ("neo4j", "password"))
    processor = LoginEventProcessor(graph_database)
    processor.process(event)