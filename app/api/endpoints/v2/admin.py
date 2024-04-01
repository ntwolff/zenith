"""
Administrative endpoints for pushing data to the stream.
"""

from fastapi import APIRouter, HTTPException
from app.models.v2 import Event, RiskSignal
from app.stream.topic import event_topic, risk_signal_topic

# Initialize router
router = APIRouter()


@router.post("/event", summary="Create a new event", response_model=None, status_code=201)
def create_event(event: Event):
    """
    Create a new event.

    This endpoint allows you to create a new event by providing the necessary details.

    - **event**: Device, IP address, customer, and (optionally) application data.

    Returns:
    - A success message indicating that the event was processed successfully.

    Raises:
    - HTTPException (status_code=400): If the provided event data is invalid.
    """
    try:
        event_topic.send(value=event)
        return {"message": "Event pushed to topic"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/risk-signal", response_model=None, status_code=201)
def create_risk_signal(risk_signal: RiskSignal):
    """
    Create a new risk signal.

    This endpoint allows you to create a new risk signal by providing the necessary details.

    - **risk_signal**: The risk signal data including type, and event information.

    Returns:
    - A success message indicating that the risk signal was processed successfully.

    Raises:
    - HTTPException (status_code=400): If the provided risk signal data is invalid.
    """
    try:
        risk_signal_topic.send(value=risk_signal)
        return {"message": "Risk signal pushed to topic"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    