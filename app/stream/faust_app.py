import faust
from app.config.settings import settings

# Faust app
## Autodiscovery https://faust-streaming.github.io/faust/userguide/settings.html#autodiscover
app = faust_app = faust.App(
    settings.faust_app_name,
    broker=settings.faust_broker,
    web_enabled=False,
    autodiscover=True,
    origin="app.stream",
    topic_partitions=settings.kafka_topic_partitions,
    topic_replication_factor=settings.kafka_topic_replication_factor,
    topic_allow_declare=True,
    consumer_auto_offset_reset="latest",
)