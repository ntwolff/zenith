from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic, event_topic
from app.stream.table import ip_velocity_table, login_velocity_table
from app.models.v2 import RiskSignal, RiskSignalType, CustomerEventType
from uuid import uuid4
from app.stream.utils.logger import log_agent_message

def get_event_ip_address(event):
    return event.ip_address.ipv4

def get_customer_uid(event):
    return event.customer.uid

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
            log_agent_message("ip_velocity", event_topic, event)


@faust_app.agent(event_topic)
async def login_velocity(events):
    async for event in events.group_by(get_customer_uid, name='customer_uid'):
        if not event.type == CustomerEventType.CUSTOMER_LOGIN:
            return
        login_velocity_table[event.customer.uid] += 1
        if ip_velocity_table[event.customer.uid].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                type=RiskSignalType.LOGIN_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)
            log_agent_message("ip_velocity", event_topic, event)