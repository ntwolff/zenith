"""
FastAPI Admin Endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from app.services.utils import BulkEventUploadService
from app.services import EventService
from app.models import Event, RiskSignal
from app.stream.topics import event_topic, risk_signal_topic

router = APIRouter()

# ----------------------------------------------
# Endpoints
# ----------------------------------------------

@router.get("/events", summary="Get a list of recent events", response_model=List[Event])
async def get_events(limit: int = 10):
    service = EventService()
    events = service.get_events(limit=limit)
    return events


@router.post("/events", summary="Trigger an event")
def create_event(event: Event):
    event_topic.send(value=event)
    return {"message": "Event pushed to topic"}


@router.post("/events/upload", summary="Upload events in bulk (.csv)")
async def bulk_upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Bulk upload a CSV of events.
    """
    service = BulkEventUploadService()
    background_tasks.add_task(service.process_file, file.file)
    return {"message": "Bulk upload started. Processing the file in the background."}


@router.post("/risk-signals", summary="Trigger a risk signal")
def create_risk_signal(risk_signal: RiskSignal):
    risk_signal_topic.send(value=risk_signal)
    return {"message": "Risk signal pushed to topic"}
