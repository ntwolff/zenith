from app.stream.faust_app import faust_app
from app.stream.topic import application_event_topic
from app.stream.utils.graph_event_processor import GraphEventProcessor
from app.database.neo4j_database import Neo4jDatabase

db = Neo4jDatabase()
processor = GraphEventProcessor(db=Neo4jDatabase())

@faust_app.agent(application_event_topic)
async def ingest_application_event(events):
    async for event in events:
        processor.process_event(event)