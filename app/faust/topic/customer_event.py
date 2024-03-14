from app.faust.app import faust_app
from app.models import CustomerEvent
from app.config.settings import settings

customer_event_topic = faust_app.topic('customer_event', value_type=CustomerEvent, partitions=settings.kafka_topic_partitions)