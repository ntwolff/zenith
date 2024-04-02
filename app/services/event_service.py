"""
Event Service
"""

from app.services._base import BaseService
from app.models import Event

class EventService(BaseService):
    def create_record(self, event: Event):
        properties = {
            "uid": event.uid,
            "event_type": event.event_type,
            "timestamp": event.timestamp
        }
        label = event.__class__.__name__
        super().create(label, properties)
