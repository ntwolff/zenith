from app.faust.app import faust_app
from app.models import GraphTask
from app.config.settings import settings

graph_management_topic = faust_app.topic('graph_management', value_type=GraphTask, partitions=settings.kafka_topic_partitions)