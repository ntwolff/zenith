"""
Event Codec
"""
import logging
from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import JsonMessageSerializer
from app.config.settings import settings
from app.models.v2 import Event


class EventSerializer(codecs.Codec):
    def __init__(self):
        self.schema_subject = "zenith-event"
        self.json_schema = self._get_json_schema()
        self.json_serializer = self._get_json_serializer()
        super().__init__()


    def _dumps(self, s: Event) -> bytes:     
        return self.json_serializer.encode_record_with_schema(
            self.schema_subject,
            self.json_schema,
            s.model_dump(mode="json")
            )


    def _loads(self, s: bytes) -> Event:     
        decoded_message = self.json_serializer.decode_message(s)
        return Event(**decoded_message)


    def _get_json_schema(self):
        return schema.JsonSchema(Event.model_json_schema())


    def _get_json_serializer(self):
        client = SchemaRegistryClient(url=settings.kafka_schema_registry_url)
        return JsonMessageSerializer(client)
