from fastapi import APIRouter
from app.api.models import CustomerEventModel
from app.models import CustomerEvent, Customer, Address, Device, IpAddress
from app.processors import CustomerEventGraphProcessor
from app.api.endpoints import graph_database

router = APIRouter()

@router.post("/customer-event")
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
    processor = CustomerEventGraphProcessor(graph_database)
    processor.process(faust_event)