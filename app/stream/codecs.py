from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import JsonMessageSerializer
from app.config.settings import settings
from pydantic import BaseModel
from app.models.event import Event
from app.models.fraud import RiskSignal


class ModelSerializer(codecs.Codec):
    def __init__(self, model: BaseModel, schema_subject: str):
        self.model = model
        self.schema_subject = schema_subject
        self.json_schema = self._get_json_schema()
        self.json_serializer = self._get_json_serializer()
        super().__init__()

    def _dumps(self, s: BaseModel) -> bytes:     
        return self.json_serializer.encode_record_with_schema(
            self.schema_subject,
            self.json_schema,
            s.model_dump(mode="json")
        )

    def _loads(self, s: bytes) -> BaseModel:     
        decoded_message = self.json_serializer.decode_message(s)
        return self.model(**decoded_message)

    def _get_json_schema(self):
        return schema.JsonSchema(self.model.model_json_schema())

    def _get_json_serializer(self):
        client = SchemaRegistryClient(url=settings.kafka.kafka_schema_registry_url)
        return JsonMessageSerializer(client)


#---------------------------------------------
# Model Codec Instances
#---------------------------------------------

def event_codec():
    return ModelSerializer(Event, "zenith-event")

def risk_signal_codec():
    return ModelSerializer(RiskSignal, "zenith-risk-signal")


# ---------------------------------------------
# Manual Faust Codec Registration
# (Auto Registration @ `faust.codecs` -> ./setup.py )
# ---------------------------------------------
codecs.register("json-events", event_codec)
codecs.register("json-risk-signals", risk_signal_codec)
