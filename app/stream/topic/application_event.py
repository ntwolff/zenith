from app.stream.faust_app import faust_app
from app.models.event import ApplicationEvent

application_event_topic = faust_app.topic('application_event', value_type=ApplicationEvent)