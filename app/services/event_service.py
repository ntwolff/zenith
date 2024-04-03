from app.services.base import GraphService
from app.models import Event

class EventService(GraphService):
    def create_record(self, event: Event):
        properties = {
            "uid": event.uid,
            "event_type": event.event_type,
            "timestamp": event.timestamp
        }
        label = event.__class__.__name__
        super().create(label, properties)


    def get_events(limit: int = 10):
        query = """
            MATCH (e:Event)
            RETURN e
            LIMIT $limit
        """
        return super().db.execute_query(query, limit=limit) # @TODO - Push to GraphService
