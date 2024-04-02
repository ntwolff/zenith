"""
Faust Kafka Topics
"""
from app.stream.faust_app import faust_app

event_topic = faust_app.topic(
    'event', 
    value_serializer='json_events')

risk_signal_topic = faust_app.topic(
    'risk_signal', 
    value_serializer='json_risk_signals')

admin_task_topic = faust_app.topic(
    'admin_task', 
    value_serializer='json_admin_tasks')