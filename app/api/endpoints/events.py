from fastapi import APIRouter
from app.models import CustomerEvent, Customer, Address, Device, IpAddress, CustomerEventModel
from app.processors import CustomerEventGraphProcessor
from app.api.endpoints import graph_database

router = APIRouter()

@router.post("/customer-event")
def handle_customer_event(event: CustomerEventModel):
    print(f"Received event: {event}")

    faust_event = CustomerEvent.from_model(event)
    processor = CustomerEventGraphProcessor(graph_database)
    processor.process(faust_event)