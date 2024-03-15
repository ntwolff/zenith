from app.faust.app import faust_app
from app.models import RiskSignal
from app.config.settings import settings

risk_signal_topic = faust_app.topic('risk_signal', value_type=RiskSignal, partitions=settings.kafka_topic_partitions)