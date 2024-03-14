from .base_service import BaseService
from app.models.event import Event

class EventService(BaseService):
    def create_record(self, event: Event):
        properties = {
            "uid": event.uid,
            "event_id": event.event_id,
            "type": event.type,
            "timestamp": event.timestamp
        }
        label = event.__class__.__name__
        super().create(label, properties)