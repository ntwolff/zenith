from app.faust.app import faust_app
from app.faust.topic.customer_event import customer_event_topic
from app.processors.graph_processor import GraphProcessor
from app.database.neo4j_database import Neo4jDatabase
import faust

@faust_app.agent(customer_event_topic)
async def ingest_event(events):
    async for event in events:
        processor = GraphProcessor(Neo4jDatabase())
        processor.process(event)