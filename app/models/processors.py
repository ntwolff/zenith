import faust

class HighVelocityEvent(faust.Record, serializer='json'):
    type: str
    id: str
    event_id: str
    event_type: str