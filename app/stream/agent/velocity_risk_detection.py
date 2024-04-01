from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic, event_topic
from app.stream.table import ip_velocity_table, login_velocity_table
from app.models.v2 import Event, RiskSignal, RiskSignalType, CustomerEventType, ApplicationEventType
from uuid import uuid4
import logging

def get_event_ip_address(event):
    return event.ip_address.ipv4

@faust_app.agent(event_topic)
async def detect_ip_velocity_risk_signal(events):
    async for event in events.group_by(get_event_ip_address, name='ip_address'):
        ip_velocity_table[event.ip_address.ipv4] += 1
        if ip_velocity_table[event.ip_address.ipv4].now() > 1:
            payload = RiskSignal(
                uid=str(uuid4()),
                type=RiskSignalType.IP_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)

            logging.info(f"Risk signal: {ip_velocity_table[event.ip_address.ipv4].now()} events in the past 5 minutes for ip addr: {event.ip_address.ipv4}")


# @faust_app.agent(event_topic)
# async def detect_login_velocity_risk_signal(events):
#     async for event in events.group_by(Event.customer.uid):
#         if not event.type == CustomerEventType.CUSTOMER_LOGIN:
#             return
#         login_velocity_table[event.customer.uid] += 1
#         if ip_velocity_table[event.customer.uid].now() > 1:
#             payload = RiskSignal(
#                 signal=CustomerEventType.LOGIN_VELOCITY,
#                 event=event
#             )
#             await risk_signal_topic.send(value=payload)

#             logging.info(f"Risk signal: {login_velocity_table[event.customer.uid].now()} events in the past 5 minutes for ip addr: {event.customer.uid}")