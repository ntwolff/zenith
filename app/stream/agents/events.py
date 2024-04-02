"""
Faust Agents - Customer/Application Events
"""
from uuid import uuid4
from app.stream.faust_app import faust_app
from app.stream.topics import risk_signal_topic, event_topic
from app.stream.tables import ip_velocity_table, login_velocity_table
from app.models.fraud import RiskSignal, RiskSignalType
from app.models.event import Event, CustomerEventType
from app.database.neo4j_database import Neo4jDatabase
from app.stream.utils.loggers import agent_logger
from app.stream.utils.processors import GraphEventProcessor


# ----------------------
# Db Initialization
# ----------------------

db = Neo4jDatabase()
processor = GraphEventProcessor(db=Neo4jDatabase())


# ----------------------
# Agent Definitions
# ----------------------

@faust_app.agent(event_topic)
async def event_ingestion(events):
    async for event in events:
        processor.process_event(event)
        agent_logger("event_ingestion", event_topic, event)


@faust_app.agent(event_topic)
async def ip_velocity_detection(events):
    async for event in events.group_by(get_event_ip_address, name='ip_address'):
        ip_velocity_table[event.ip_address.ipv4] += 1
        if ip_velocity_table[event.ip_address.ipv4].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                signal_type=RiskSignalType.IP_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)
            agent_logger('ip_velocity_detection', event_topic, event)


@faust_app.agent(event_topic)
async def login_velocity_detection(events):
    async for event in events.group_by(get_customer_uid, name='customer'):
        if not event.event_type == CustomerEventType.CUSTOMER_LOGIN:
            continue
        login_velocity_table[event.customer.uid] += 1
        if login_velocity_table[event.customer.uid].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                signal_type=RiskSignalType.LOGIN_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)
            agent_logger('login_velocity_detection', event_topic, event)


# ----------------------
# Helper Functions
# ----------------------

async def get_event_ip_address(event:Event) -> str:
    return event.ip_address.ipv4


async def get_customer_uid(event:Event) -> str:
    return event.customer.uid