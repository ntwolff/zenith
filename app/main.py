import logging
import faust
from app.models import CustomerRegistrationEvent, EscalationEvent

# FAUST APP
app = faust.App('zenith', broker='kafka://localhost:9092')
app.conf.logging_level = logging.INFO


## KAFKA TOPICS
customer_registered_topic = app.topic('event__customer_registration', value_type=CustomerRegistrationEvent)
escalation_topic = app.topic('event__escalation', value_type=EscalationEvent)


