from fastapi import APIRouter, HTTPException
from app.models import CustomerEvent, CustomerEventModel, ApplicationEventModel, ApplicationEvent
from app.database.neo4j_database import Neo4jDatabase
from app.stream.topic import event_topic

router = APIRouter()
graph_database = Neo4jDatabase()

@router.post("/customer-event", summary="Create a new CustomerEvent", response_model=None, status_code=201)
def create_customer_event(event: CustomerEventModel):
    """
    Create a new customer event.

    This endpoint allows you to create a new customer event by providing the necessary event details.

    - **event**: The customer event data including customer information, device information, and IP address.

    Returns:
    - A success message indicating that the event was processed successfully.

    Raises:
    - HTTPException (status_code=400): If the provided event data is invalid.
    """
    try:
        faust_event = CustomerEvent.from_model(event)
        event_topic.send(value=faust_event)
        return {"message": "Event pushed to topic"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/application-event", summary="Create a new ApplicationEvent", response_model=None, status_code=201)
def create_application_event(event: ApplicationEventModel):
    """
    Create a new application event.

    This endpoint allows you to create a new application event by providing the necessary event details.

    - **event**: The application event data.

    Returns:
    - A success message indicating that the event was processed successfully.

    Raises:
    - HTTPException (status_code=400): If the provided event data is invalid.
    """
    try:
        faust_event = ApplicationEvent.from_model(event)
        event_topic.send(value=faust_event)
        return {"message": "Event pushed to topic"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))