import faust
import abc
from app.config.settings import settings
from typing import Any, Type
from pydantic import TypeAdapter, GetCoreSchemaHandler, BaseModel, ConfigDict
from pydantic_core import core_schema
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers.faust import FaustJsonSerializer


class AbstractBaseModel(BaseModel, abc.ABC):
    model_config = ConfigDict(arbitrary_types_allowed = True)


class AbstractBaseRecord(faust.Record, abstract=True):
    this: AbstractBaseModel

    @classmethod
    def __get_pydantic_core_schema__(
        self, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        #assert source is AbstractBaseRecord
        if not source.this:
            raise ValueError('The Record must have a field named this')
        #assert source is AbstractBaseModel
        schema = handler(source.this.type)
        return core_schema.typed_dict_schema(
            {
                'this': core_schema.typed_dict_field(core_schema.model_ser_schema(source.this.type, schema)),
            },
        )
    

class RecordFactory:
    def __init__(self, model_class: Type[AbstractBaseModel]):
        self.model_class = model_class
        self.record_class = self._create_record_class()
        self.codec = self._create_codec()

    def _create_record_class(self) -> Type[AbstractBaseRecord]:
        record_class_name = f"{self.model_class.__name__}Record"
        record_class = type(record_class_name, (AbstractBaseRecord,), {
            'this': self.model_class,
            '__annotations__': {'this': self.model_class},
            '__serializer__': f'{self.model_class.__name__.lower()}_codec'
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

    def get_record_class(self) -> Type[AbstractBaseRecord]:
        return self.record_class

    def get_codec(self):
        return self.codec