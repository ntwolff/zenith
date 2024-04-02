"""
Event Ingestion Agents
"""

from app.stream.faust_app import faust_app
from app.stream.topic import event_topic
from app.stream.util.processors import GraphEventProcessor
from app.database.neo4j_database import Neo4jDatabase
from app.stream.util.loggers import agent_logger

db = Neo4jDatabase()
processor = GraphEventProcessor(db=Neo4jDatabase())

@faust_app.agent(event_topic)
async def event_ingestion(events):
    async for event in events:
        processor.process_event(event)
        agent_logger("event_ingestion", event_topic, event)
