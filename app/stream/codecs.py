from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers.faust import FaustJsonSerializer
from pydantic import TypeAdapter
from app.config.settings import settings

from app.models.foo import FooRecord

# create an instance of the `SchemaRegistryClient`
schema_registry_url = settings.kafka_schema_registry_url
client = SchemaRegistryClient(url=f"{schema_registry_url}")

record_type = FooRecord
record_schema = TypeAdapter(record_type).json_schema()

subject = record_type.__name__.lower()
json_foo_serializer = FaustJsonSerializer(client, subject, record_schema)
schema_id = client.register(subject, schema.JsonSchema(record_schema))

# print(f"Registry url: {schema_registry_url}")
# print(f"Schema subject: {subject}")
# print(f"Schema definition: {record_schema}")
# print (f"Schema identifier: {schema_id}")

def json_foo_codec():
    return json_foo_serializer