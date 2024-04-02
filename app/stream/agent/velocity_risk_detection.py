"""
Velocity Risk Detection Agents
"""

from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic, event_topic
from app.stream.table import ip_velocity_table, login_velocity_table
from app.models.v2.fraud import RiskSignal, RiskSignalType
from app.models.v2.event import Event, CustomerEventType
from uuid import uuid4
from app.stream.util.loggers import agent_logger


@faust_app.agent(event_topic)
async def ip_velocity(events):
    async for event in events.group_by(get_event_ip_address, name='ip_address'):
        ip_velocity_table[event.ip_address.ipv4] += 1
        if ip_velocity_table[event.ip_address.ipv4].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                type=RiskSignalType.IP_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)
            agent_logger(RiskSignalType.IP_VELOCITY.value, event_topic, event)


@faust_app.agent(event_topic)
async def login_velocity(events):
    async for event in events.group_by(get_customer_uid, name='customer'):
        if not (event.type == CustomerEventType.CUSTOMER_LOGIN.value):
            continue
        else:
            login_velocity_table[event.customer.uid] += 1
            if login_velocity_table[event.customer.uid].now() > 1:
                payload = RiskSignal(
                    uid=str(uuid4()),
                    type=RiskSignalType.LOGIN_VELOCITY,
                    event=event
                )
                await risk_signal_topic.send(value=payload)
                agent_logger(RiskSignalType.LOGIN_VELOCITY.value, event_topic, event)


async def get_event_ip_address(event:Event) -> str:
    return event.ip_address.ipv4


async def get_customer_uid(event:Event) -> str:
    return event.customer.uid
