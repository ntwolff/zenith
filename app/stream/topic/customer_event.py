from app.stream.faust_app import faust_app
from app.models import CustomerEvent

customer_event_topic = faust_app.topic('customer_event', value_type=CustomerEvent)