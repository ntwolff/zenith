"""
Event Service
"""

from app.services.base_service import BaseService
from app.models.v2 import Event

class EventService(BaseService):
    def create_record(self, event: Event):
        properties = {
            "uid": event.uid,
            "type": event.type,
            "timestamp": event.timestamp
        }
        label = event.__class__.__name__
        super().create(label, properties)