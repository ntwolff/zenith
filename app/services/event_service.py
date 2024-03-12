from .base_service import BaseService
from app.models.event import Event

class EventService(BaseService):
    def create(self, event: Event):
        query = """
            CREATE (e:Event {id: $id, type: $type, timestamp: $timestamp})
        """
        self.db.execute_query(query, id=event.id, type=event.type, timestamp=event.timestamp)

    def create_relationship(self, event: Event, related_object, relationship_type: str):
        query = f"""
            MATCH (e:Event {{id: $event_id}})
            MATCH (o {{id: $object_id}})
            MERGE (e)-[r:{relationship_type}]->(o)
        """
        self.db.execute_query(query, event_id=event.id, object_id=related_object.id)