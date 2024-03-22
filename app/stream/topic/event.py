from app.stream.faust_app import faust_app
from app.models.v2 import Event

event_topic = faust_app.topic('event', value_type=Event)