# from app.models.v2.base import RecordFactory
# from app.models.v2.foo import Foo
# from app.models.v2.bar import Bar
# from app.models.v2 import Event, RiskSignal, GraphTask
# from app.config.settings import settings
# from schema_registry.client import SchemaRegistryClient
# from schema_registry.serializers.faust import FaustJsonSerializer
# # Import other model classes as needed

# # foo_factory = RecordFactory(Foo, hydrate=True)
# # bar_factory = RecordFactory(Bar, hydrate=True)
# # event_factory = RecordFactory(Event, hydrate=True)
# # risk_signal_factory = RecordFactory(RiskSignal, hydrate=True)
# # graph_task_factory = RecordFactory(GraphTask, hydrate=True)
# # # Create factories for other model classes as needed

# # def foo_codec():
# #     return foo_factory.get_codec()

# # def bar_codec():
# #     return bar_factory.get_codec()

# # def event_codec():
# #     return event_factory.get_codec()

# # def risk_signal_codec():
# #     return risk_signal_factory.get_codec()

# # def graph_task_codec():
# #     return graph_task_factory.get_codec()

# schema_registry_url = settings.kafka_schema_registry_url
# client = SchemaRegistryClient(url=f"{schema_registry_url}")

# json_name = 'json_event' 
# json_schema = Event.model_json_schema()
# faust_serializer = FaustJsonSerializer(client, json_name, json_schema)

# def event_codec():
#     return faust_serializer

# # Define codec functions for other model classes as needed