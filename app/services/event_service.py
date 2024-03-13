from .base_service import BaseService
from app.models.event import Event

class EventService(BaseService):
    def create(self, event: Event):
        query = """
            CREATE (e:Event {event_id: $id, type: $type, timestamp: $timestamp})
        """
        self.db.execute_query(query, id=event.event_id, type=event.type, timestamp=event.timestamp)

    def create_relationship(self, event: Event, related_obj_key: str, related_obj_value: str, relationship_type: str):
        query = f"""
            MATCH (e:Event {{event_id: $event_id}})
            MATCH (o {{{related_obj_key}: $related_obj_value}})
            MERGE (e)-[r:{relationship_type}]->(o)
        """
        self.db.execute_query(query, event_id=event.event_id, related_obj_value=related_obj_value)