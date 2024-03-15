from app.faust.app import faust_app
from app.models.event import ApplicationEvent
from app.config.settings import settings

application_event_topic = faust_app.topic('application_event', value_type=ApplicationEvent, partitions=settings.kafka_topic_partitions)