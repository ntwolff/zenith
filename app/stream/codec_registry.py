# app/stream/codec_registry.py

from app.models.v2.base import RecordFactory
from app.models.v2.foo import Foo
from app.models.v2.bar import Bar
from app.models.v2 import CustomerEvent, ApplicationEvent, RiskSignal, GraphTask
# Import other model classes as needed

foo_factory = RecordFactory(Foo)
bar_factory = RecordFactory(Bar)
customer_event_factory = RecordFactory(CustomerEvent)
application_event_factory = RecordFactory(ApplicationEvent)
risk_signal_factory = RecordFactory(RiskSignal)
graph_task_factory = RecordFactory(GraphTask)
# Create factories for other model classes as needed

def foo_codec():
    return foo_factory.get_codec()

def bar_codec():
    return bar_factory.get_codec()

def customer_event_codec():
    return customer_event_factory.get_codec()

def application_event_codec():
    return application_event_factory.get_codec()

def risk_signal_codec():
    return risk_signal_factory.get_codec()

def graph_task_codec():
    return graph_task_factory.get_codec()

# Define codec functions for other model classes as needed