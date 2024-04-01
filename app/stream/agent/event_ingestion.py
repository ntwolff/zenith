from app.stream.faust_app import faust_app
from app.stream.topic import event_topic
from app.stream.utils.graph_event_processor import GraphEventProcessor
from app.database.neo4j_database import Neo4jDatabase
from app.stream.utils.logger import log_agent_message

db = Neo4jDatabase()
processor = GraphEventProcessor(db=Neo4jDatabase())

@faust_app.agent(event_topic)
async def event_ingestion(events):
    async for event in events:
        processor.process_event(event)
        log_agent_message("event_ingestion", event_topic, event)