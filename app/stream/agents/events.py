from uuid import uuid4
import random
from app.stream.faust_app import faust_app
from app.stream.topics import risk_signal_topic, event_topic
from app.stream.tables import ip_velocity_table, login_velocity_table
from app.models.fraud import RiskSignal, RiskSignalType
from app.models.event import Event, CustomerEventType, ApplicationEventType
from app.stream.utils.loggers import agent_logger
from app.stream.utils.processors import GraphEventProcessor
from app.database.manager import DatabaseManager
from app.database.repositories.graph import GraphRepository
from app.config.settings import settings


# ----------------------
# Init
# ----------------------

db_manager = DatabaseManager(settings)
graph_repo = GraphRepository(db_manager)
processor = GraphEventProcessor(db=graph_repo.db)


# ----------------------
# Agents
# ----------------------

def process_event(event):
    if (event.event_type not in CustomerEventType) and (event.event_type not in ApplicationEventType):
        raise ValueError(f"Invalid event type: {event.event_type}")
    if event.customer is None or event.device is None or event.ip_address is None:
        raise ValueError("Missing required event fields")
    processor.process_event(event)


@faust_app.agent(event_topic)
async def event_ingestion(events):
    async for event in events:
        try:
            process_event(event)
            agent_logger("event_ingestion", event_topic, event)
        except ValueError as e:
            agent_logger("event_ingestion", event_topic, event, warning=str(e))


@faust_app.agent(event_topic)
async def ip_velocity_detection(events):
    async for event in events.group_by(get_event_ip_address, name='ip_address'):
        ip_velocity_table[event.ip_address.ipv4] += 1
        if ip_velocity_table[event.ip_address.ipv4].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                signal_type=RiskSignalType.IP_VELOCITY,
                event=event,
                fraud_score=random.uniform(0.1, 0.9)
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
                event=event,
                fraud_score=random.uniform(0.1, 0.9)
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
