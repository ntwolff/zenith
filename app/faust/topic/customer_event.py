from app.faust.app import faust_app
from app.models import CustomerEvent

customer_event_topic = faust_app.topic('customer_event', value_type=CustomerEvent)