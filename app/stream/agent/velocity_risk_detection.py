from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic, event_topic
from app.stream.table import ip_velocity_table, login_velocity_table
from app.models.v2 import Event, RiskSignal, RiskSignalType, CustomerEventType, ApplicationEventType
from uuid import uuid4
import logging

# EventRecord = RecordFactory(Event).get_record_class()

# Anonymous send to other agent after grabbing record
# @app.agent(key_type=Point, value_type=Point)
# async def my_agent(events):
#     async for event in events:
#         print(event)

# @faust_app.agent(event_topic)
# async def detect_ip_velocity_risk_signal(records):
#     async for record in records.group_by(Event(this=EventRecord.this).ip_address.ipv4):
#         event = Event(record.this)
#         ip_velocity_table[event.ip_address.ipv4] += 1
#         if ip_velocity_table[event.ip_address.ipv4].now() > 1:
#             payload = RiskSignal(
#                 uid=uuid4(),
#                 signal=RiskSignalType.IP_VELOCITY,
#                 event=event
#             )
#             await risk_signal_topic.send(value=payload)

#             logging.info(f"Risk signal: {ip_velocity_table[event.ip_address.ipv4].now()} events in the past 5 minutes for ip addr: {event.ip_address.ipv4}")


# @faust_app.agent(event_topic)
# async def detect_login_velocity_risk_signal(records):
#     async for record in records.group_by(Event(this=EventRecord.this).ip_address.ipv4):
#         event = Event(record.this)
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