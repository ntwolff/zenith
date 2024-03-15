from app.faust.app import faust_app
from app.faust.topic import risk_signal_topic, customer_event_topic
from app.faust.table import ip_velocity_table, login_velocity_table
from app.models import CustomerEvent, RiskSignal, SignalEnum
from uuid import uuid4
import logging

@faust_app.agent(customer_event_topic)
async def detect_ip_velocity_risk_signal(events):
    async for event in events.group_by(CustomerEvent.ip_address.uid):
        ip_velocity_table[event.ip_address.uid] += 1
        if ip_velocity_table[event.ip_address.uid].now() > 1:
            payload = RiskSignal(
                uid=uuid4(),
                signal=SignalEnum.IP_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)

            logging.info(f"Risk signal: {ip_velocity_table[event.ip_address.uid].now()} events in the past 5 minutes for ip addr: {event.ip_address.uid}")

@faust_app.agent(customer_event_topic)
async def detect_login_velocity_risk_signal(events):
    async for event in events.group_by(CustomerEvent.customer.uid):
        if not event.type == "login":
            return
        login_velocity_table[event.customer.uid] += 1
        if ip_velocity_table[event.customer.uid].now() > 1:
            payload = RiskSignal(
                signal=SignalEnum.LOGIN_VELOCITY,
                event=event
            )
            await risk_signal_topic.send(value=payload)

            logging.info(f"Risk signal: {login_velocity_table[event.customer.uid].now()} events in the past 5 minutes for ip addr: {event.customer.uid}")