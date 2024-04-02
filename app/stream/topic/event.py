"""
Event Topic
"""
from app.stream.faust_app import faust_app

event_topic = faust_app.topic('event', value_serializer='event_serializer')
