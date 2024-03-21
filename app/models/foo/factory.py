# /app/models/foo/factory.py

from typing import Type
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers.faust import FaustJsonSerializer
from pydantic import TypeAdapter
from app.config.settings import settings
from app.models.foo.base_model import ZenithBaseModel
from app.models.foo.base_record import ZenithBaseRecord

class RecordFactory:
    def __init__(self, model_class: Type[ZenithBaseModel]):
        self.model_class = model_class
        self.record_class = self._create_record_class()
        self.codec = self._create_codec()

    def _create_record_class(self) -> Type[ZenithBaseRecord]:
        record_class_name = f"{self.model_class.__name__}Record"
        record_class = type(record_class_name, (ZenithBaseRecord,), {
            'this': self.model_class,
            '__annotations__': {'this': self.model_class},
            '__serializer__': f'json_{self.model_class.__name__.lower()}s'
        })
        return record_class

    def _create_codec(self):
        schema_registry_url = settings.kafka_schema_registry_url
        client = SchemaRegistryClient(url=f"{schema_registry_url}")

        record_schema = TypeAdapter(self.record_class).json_schema()

        subject = self.record_class.__name__.lower()
        json_serializer = FaustJsonSerializer(client, subject, record_schema)
        schema_id = client.register(subject, schema.JsonSchema(record_schema))

        def json_codec_callable():
            return json_serializer

        return json_codec_callable

    def get_record_class(self) -> Type[ZenithBaseRecord]:
        return self.record_class

    def get_codec(self):
        return self.codec